# LocalVLM-FastAPI-Demo

[简体中文](./README.md) | [English](./README_EN.md)

---

A compact local multimodal inference demo built with `vLLM` and `FastAPI`.

This project turns a locally served Qwen model into a small but complete demo application with:

- `POST /api/chat/text` for text chat
- `POST /api/chat/file` for text-file understanding
- `POST /api/chat/image` for image understanding
- `GET /health` for health checks
- `GET /` and `/web/index.html` for a browser demo UI

The browser demo supports:

- text input
- uploading `.txt`, `.md`, `.json`, and `.csv` files
- selecting or taking photos on mobile devices
- client-side image compression in the browser
- streaming and non-streaming responses
- Markdown and MathJax rendering
- access from phones on the same local network

This repository is suitable as:

- a starter project for local LLM deployment practice
- a vLLM + FastAPI integration example
- an OpenAI-compatible API wrapper demo
- a browser-based validation layer before building a mobile app

## Project Goal

The purpose of this project is not to build a complex frontend. The goal is to package a local model inference service into a clean, reproducible, and easy-to-extend engineering demo.

You can think of it as three layers:

1. `vLLM`: loads the model and exposes an OpenAI-compatible API
2. `FastAPI`: organizes the model capability into clear business endpoints
3. `Web UI`: provides browser-based interaction for text, file, and image inputs

## Project Structure

```text
test_code/
├── fastapi_server/
│   ├── main.py
│   ├── config.py
│   ├── services/
│   │   └── vllm_client.py
│   ├── web/
│   │   └── index.html
│   ├── uploads/
│   └── logs/
├── scripts/
│   ├── start_vllm.sh
│   ├── start_fastapi.sh
│   └── test_curl.sh
├── README.md
└── README_EN.md
```

Key files:

- `fastapi_server/main.py`: FastAPI entry point and API routes
- `fastapi_server/services/vllm_client.py`: wrapper around the local vLLM OpenAI-compatible endpoint
- `fastapi_server/web/index.html`: browser demo page
- `scripts/start_vllm.sh`: starts the vLLM server
- `scripts/start_fastapi.sh`: starts the FastAPI server
- `scripts/test_curl.sh`: simple API smoke test

## Tech Stack

Backend:

- Python
- FastAPI
- Uvicorn
- OpenAI Python SDK
- vLLM

Frontend:

- HTML
- CSS
- JavaScript
- `marked.js` for Markdown rendering
- `MathJax` for math rendering

Model service:

- `Qwen3.5-0.8B-int4-AutoRound`
- vLLM OpenAI-compatible API

## Implemented Features

### 1. Text Chat

The frontend sends a prompt to `POST /api/chat/text`, and FastAPI forwards it to the local vLLM service.

Typical uses:

- basic chat
- summarization
- structured Q&A
- Markdown output

### 2. File Understanding

The frontend currently supports these text-based file types:

- `.txt`
- `.md`
- `.json`
- `.csv`

The browser reads the file content first, then sends `file_name`, `file_content`, and `question` to `POST /api/chat/file`.

On the backend, the file content is wrapped into a prompt so the model can read the file before answering the question.

Current limitation:

- the backend truncates file content to the first `6000` characters to keep inference stable

### 3. Image Understanding

The frontend supports:

- selecting an image on desktop
- taking a photo or selecting one on mobile

Images are not uploaded in raw form. The browser first:

1. reads the image
2. resizes it so the longest side is at most `768`
3. converts it to JPEG base64
4. sends it to `POST /api/chat/image`

Benefits of this approach:

- lower bandwidth usage
- smaller request payloads
- better success rate on mobile browsers

### 4. Streaming and Non-Streaming Output

The UI includes a switch between streaming and non-streaming modes.

- Non-streaming: returns the full answer at once
- Streaming: FastAPI uses `StreamingResponse` to push generated text progressively

### 5. Mobile Browser Access

As long as:

- vLLM listens on `0.0.0.0`
- FastAPI listens on `0.0.0.0`
- the phone and computer are on the same LAN

You can open the demo from a phone browser with:

```text
http://<your-lan-ip>:9000/web/index.html
```

## API Overview

### `GET /`

Example response:

```json
{
  "message": "Qwen Mobile Demo is running",
  "web_demo": "/web/index.html"
}
```

### `GET /health`

Example response:

```json
{
  "status": "ok"
}
```

### `POST /api/chat/text`

Example request:

```json
{
  "prompt": "Hello, please introduce yourself.",
  "max_tokens": 1024,
  "temperature": 0.7,
  "stream": false
}
```

Example response:

```json
{
  "code": 200,
  "type": "text",
  "answer": "..."
}
```

### `POST /api/chat/file`

Example request:

```json
{
  "file_name": "demo.md",
  "file_content": "# Title\nThis is the file content.",
  "question": "Please summarize this file.",
  "max_tokens": 256,
  "temperature": 0.7,
  "stream": false
}
```

Example response:

```json
{
  "code": 200,
  "type": "file",
  "answer": "..."
}
```

### `POST /api/chat/image`

Example request:

```json
{
  "prompt": "Please describe the main content of this image.",
  "image_base64": "data:image/jpeg;base64,...",
  "max_tokens": 256,
  "temperature": 0.7,
  "stream": false
}
```

Example response:

```json
{
  "code": 200,
  "type": "image",
  "answer": "..."
}
```

## Environment Assumptions

This project is currently written for a local development setup. Adjust paths and environment names to match your machine.

Default assumptions in the scripts:

- model path: `/home/zxy/codes/models/Qwen3.5-0.8B-int4-AutoRound`
- project path: `/home/zxy/codes/test_code`
- conda environment: `vllm-debug`
- vLLM port: `8001`
- FastAPI port: `9000`

Recommended environment:

- Linux or WSL2
- Python `3.10+`
- NVIDIA GPU
- CUDA dependencies installed correctly

## Installation

Create and activate your Python or conda environment first, then install dependencies:

```bash
pip install fastapi uvicorn openai python-multipart
pip install vllm
```

The frontend also uses external CDN resources:

- `marked.js`
- `MathJax`

So the browser experience is best when internet access is available.

## How to Run

### 1. Make the scripts executable

```bash
chmod +x scripts/start_vllm.sh
chmod +x scripts/start_fastapi.sh
chmod +x scripts/test_curl.sh
```

### 2. Start vLLM

```bash
./scripts/start_vllm.sh
```

Current script behavior:

- initializes conda automatically
- activates `vllm-debug`
- starts `vllm serve`
- exposes the model on `0.0.0.0:8001`

Important parameters currently used:

- `--served-model-name qwen3.5-int4`
- `--quantization autoround`
- `--gpu-memory-utilization 0.75`
- `--max-model-len 4096`
- `--tensor-parallel-size 1`
- `--disable-frontend-multiprocessing`
- `--enforce-eager`
- `--trust-remote-code`

### 3. Start FastAPI

```bash
./scripts/start_fastapi.sh
```

Current script behavior:

- initializes conda automatically
- activates `vllm-debug`
- enters `fastapi_server`
- starts Uvicorn on `0.0.0.0:9000`

### 4. Run a quick curl test

```bash
./scripts/test_curl.sh
```

## Access URLs

### Local access on the same machine

```text
http://127.0.0.1:9000/
http://127.0.0.1:9000/health
http://127.0.0.1:9000/web/index.html
```

### Access from a phone on the same LAN

First find your computer's LAN IP, for example:

```text
192.168.xxx.xxx
```

Then open:

```text
http://192.168.xxx.xxx:9000/web/index.html
```

If the UI opens but API requests fail, check these items first:

1. FastAPI is listening on `0.0.0.0`
2. vLLM is listening on `0.0.0.0`
3. local firewall and LAN settings are correct
4. WSL and Windows port forwarding is configured if needed

## Frontend Notes

The page is organized into three sections:

### Text input

- enter a prompt
- call `POST /api/chat/text`
- display the model response

### File input

- upload `.txt`, `.md`, `.json`, or `.csv`
- read file content in the browser
- call `POST /api/chat/file`
- display the summary or answer

### Image input

- supports mobile camera capture through `capture="environment"`
- supports image preview
- compresses the image in the browser before sending base64 to the backend
- calls `POST /api/chat/image`

The page also supports:

- Markdown rendering
- math formula rendering
- streaming typewriter-style output

## Known Limitations

1. File understanding only supports text-based files
2. File content is truncated to the first `6000` characters
3. Image support still depends on whether the loaded model truly has multimodal capability
4. No persistent chat history is implemented
5. No authentication is implemented

This is currently an engineering demo, not a production-ready system.

## Extension Ideas

Engineering direction:

- add request logging and tracing
- improve exception handling and unified error responses
- move configuration into environment variables or config files
- containerize the project with Docker
- add Nginx as a reverse proxy
- add CI with GitHub Actions

Inference direction:

- try larger or more capable multimodal models
- compare different quantization strategies
- benchmark TPS, first-token latency, and concurrency
- compare vLLM with other serving frameworks

Product direction:

- continue into a dedicated mobile app
- add chat history
- add a camera-first experience
- add multi-turn file Q&A

## Summary

`Qwen Local Multimodal Demo` packages a local Qwen model behind a clean FastAPI service and a lightweight browser UI. It covers text chat, file understanding, and image understanding, while also demonstrating streaming output, browser-side image compression, and phone access over a local network.

For learning local model deployment and turning raw inference into a presentable demo system, this repository is a practical intermediate step between command-line experiments and a real application.
