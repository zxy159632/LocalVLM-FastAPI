from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.vllm_client import chat_text, chat_image

app = FastAPI(title="Qwen Mobile Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app.mount("/web", StaticFiles(directory=str(WEB_DIR)), name="web")


class TextRequest(BaseModel):
    prompt: str
    max_tokens: int = 1024 # 限制模型返回tokens展示数量，超出截断
    temperature: float = 0.7
    stream: bool = False  # 新增流式开关参数


class FileRequest(BaseModel):
    file_name: str
    file_content: str
    question: str = "请总结这份文件的内容"
    max_tokens: int = 256
    temperature: float = 0.7
    stream: bool = False


class ImageRequest(BaseModel):
    prompt: str
    image_base64: str
    max_tokens: int = 256
    temperature: float = 0.7
    stream: bool = False


# 新增：用于将大模型返回的生成器转换为流式字节块的迭代器
def generate_stream(vllm_generator):
    for chunk in vllm_generator:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


@app.get("/")
def root():
    return {
        "message": "Qwen Mobile Demo is running",
        "web_demo": "/web/index.html"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat/text")
def api_chat_text(req: TextRequest):
    resp = chat_text(req.prompt, req.max_tokens, req.temperature, req.stream)
    
    if req.stream:
        # 使用 StreamingResponse 实时推流
        return StreamingResponse(generate_stream(resp), media_type="text/plain")
        
    return {
        "code": 200,
        "type": "text",
        "answer": resp
    }


@app.post("/api/chat/file")
def api_chat_file(req: FileRequest):
    prompt = f"""下面是文件内容，请先理解文件，再回答问题。

文件名：{req.file_name}

文件内容：
{req.file_content[:6000]}

问题：
{req.question}
"""
    resp = chat_text(prompt, req.max_tokens, req.temperature, req.stream)
    
    if req.stream:
        return StreamingResponse(generate_stream(resp), media_type="text/plain")
        
    return {
        "code": 200,
        "type": "file",
        "answer": resp
    }


@app.post("/api/chat/image")
def api_chat_image(req: ImageRequest):
    resp = chat_image(req.prompt, req.image_base64, req.max_tokens, req.temperature, req.stream)
    
    if req.stream:
        return StreamingResponse(generate_stream(resp), media_type="text/plain")
        
    return {
        "code": 200,
        "type": "image",
        "answer": resp
    }