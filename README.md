# 基于 vLLM + FastAPI 的本地多模态推理演示项目

一个面向**大模型部署入门 / 推理服务工程化演示**的小型项目。

本项目基于本地 `vLLM` 服务与 `FastAPI` 中间层，提供三个清晰的接口：

- `POST /api/chat/text`：文本问答
- `POST /api/chat/file`：文件理解
- `POST /api/chat/image`：图片理解
- `GET /health`：健康检查
- `GET /`：服务说明入口

前端页面支持：

- 文本输入
- 文本文件上传（txt / md / json / csv）
- 手机拍照 / 相册选图
- 浏览器端图片压缩
- 流式 / 非流式两种输出模式
- Markdown 渲染与数学公式展示

这个项目适合作为：

- 大模型部署工程师的入门项目
- vLLM 本地部署演示项目
- FastAPI + OpenAI 兼容接口中转示例
- 手机浏览器访问本地模型的 Demo
- 后续安卓 App 接入前的验证版本

---

## 1. 项目目标

本项目的核心目标不是做一个复杂的前端，而是把“**本地模型推理服务**”整理成一个结构清楚、便于演示、便于复现、便于后续扩展的工程样例。

你可以把它理解为三层：

1. **vLLM 层**：负责真正加载模型并提供 OpenAI 兼容接口
2. **FastAPI 层**：负责把能力拆成清晰的业务接口
3. **Web 层**：负责文本 / 文件 / 图片的浏览器交互

---

## 2. 项目目录结构

```text
test_code/
├─ fastapi_server/
│  ├─ main.py
│  ├─ config.py
│  ├─ services/
│  │  └─ vllm_client.py
│  ├─ web/
│  │  └─ index.html
│  ├─ uploads/
│  └─ logs/
├─ scripts/
│  ├─ start_vllm.sh
│  ├─ start_fastapi.sh
│  └─ test_curl.sh
└─ README.md
```

各目录作用：

- `fastapi_server/main.py`：FastAPI 主入口，定义路由与请求模型
- `fastapi_server/services/vllm_client.py`：封装对 vLLM 的调用
- `fastapi_server/web/index.html`：前端演示页面
- `scripts/start_vllm.sh`：启动 vLLM
- `scripts/start_fastapi.sh`：启动 FastAPI
- `scripts/test_curl.sh`：命令行接口测试

---

## 3. 技术栈

后端：

- Python
- FastAPI
- Uvicorn
- OpenAI Python SDK
- vLLM

前端：

- HTML
- CSS
- JavaScript
- marked.js（Markdown 渲染）
- MathJax（公式渲染）

模型服务：

- Qwen3.5-0.8B INT4 AutoRound
- vLLM OpenAI-compatible API

---

## 4. 当前实现的功能

### 4.1 文本问答

前端输入 prompt，后端调用 `/api/chat/text`，再由 FastAPI 转发到本地 vLLM 服务。

适合演示：

- 基础聊天
- 简单摘要
- 结构化问答
- Markdown 输出

### 4.2 文件理解

前端支持选择以下文本类文件：

- `.txt`
- `.md`
- `.json`
- `.csv`

浏览器先读取文件内容，再把 `file_name + file_content + question` 发送到 `/api/chat/file`。

后端会把文件内容拼成一个完整 prompt，让模型先理解文件再回答问题。

当前版本对文件内容做了截断控制：

- 后端默认只取前 `6000` 个字符，避免一次性塞入过长内容导致推理不稳定

### 4.3 图片理解

前端支持：

- 电脑端选择图片
- 手机端拍照或相册选择

图片不会直接原图上传，而是先在浏览器端完成：

1. 读取图片
2. 按最长边压缩（默认 768）
3. 转成 JPEG base64
4. 发送到 `/api/chat/image`

这样做的好处是：

- 降低带宽占用
- 降低请求体体积
- 提高手机网页端成功率

### 4.4 流式 / 非流式输出

页面右上角提供“流式打字机输出 / 非流式输出”切换。

- 非流式：一次性返回完整答案
- 流式：FastAPI 使用 `StreamingResponse` 持续向前端推送模型生成内容

### 4.5 手机浏览器访问

只要：

- vLLM 监听 `0.0.0.0`
- FastAPI 监听 `0.0.0.0`
- 手机和电脑在同一局域网

就可以直接在手机浏览器访问：

```text
http://你的电脑局域网IP:9000/web/index.html
```

**本地模型服务不仅能在电脑网页跑，还能直接通过手机浏览器访问。**

---

## 5. 接口说明

### 5.1 `GET /`

返回服务说明：

```json
{
  "message": "Qwen Mobile Demo is running",
  "web_demo": "/web/index.html"
}
```

### 5.2 `GET /health`

健康检查：

```json
{
  "status": "ok"
}
```

### 5.3 `POST /api/chat/text`

请求示例：

```json
{
  "prompt": "你好，请做个自我介绍",
  "max_tokens": 1024,
  "temperature": 0.7,
  "stream": false
}
```

返回示例（非流式）：

```json
{
  "code": 200,
  "type": "text",
  "answer": "..."
}
```

### 5.4 `POST /api/chat/file`

请求示例：

```json
{
  "file_name": "demo.md",
  "file_content": "# 标题\n这是文件内容",
  "question": "请总结这份文件的内容",
  "max_tokens": 256,
  "temperature": 0.7,
  "stream": false
}
```

返回示例：

```json
{
  "code": 200,
  "type": "file",
  "answer": "..."
}
```

### 5.5 `POST /api/chat/image`

请求示例：

```json
{
  "prompt": "请描述这张图片的主要内容",
  "image_base64": "data:image/jpeg;base64,...",
  "max_tokens": 256,
  "temperature": 0.7,
  "stream": false
}
```

返回示例：

```json
{
  "code": 200,
  "type": "image",
  "answer": "..."
}
```

---

## 6. 运行环境

本项目默认基于本地环境编写，实际使用时请按自己的路径调整：

- 模型路径：`{path_to}/models/Qwen3.5-0.8B-int4-AutoRound`
- 项目路径：`{path_to}/test_code`
- conda 环境：`vllm-debug`
- vLLM 服务端口：`8001`
- FastAPI 服务端口：`9000`

推荐环境：

- Linux / WSL2
- Python 3.10+
- NVIDIA GPU
- 已正确安装 CUDA 相关依赖

---

## 7. 安装依赖

先创建并激活你的 Python / conda 环境，然后安装依赖：

```bash
pip install fastapi uvicorn openai python-multipart
pip install vllm
```

前端页面中还用到了 CDN：

- `marked.js`
- `MathJax`

因此浏览器联网时体验更完整。

---

## 8. 启动方式

### 8.1 给脚本添加可执行权限

```bash
chmod +x scripts/start_vllm.sh
chmod +x scripts/start_fastapi.sh
chmod +x scripts/test_curl.sh
```

### 8.2 启动 vLLM

```bash
./scripts/start_vllm.sh
```

脚本核心逻辑：

- 自动加载 conda
- 激活 `vllm-debug`
- 使用 `vllm serve` 启动本地模型
- 开放 `0.0.0.0:8001`

当前脚本中使用的关键参数包括：

- `--served-model-name qwen3.5-int4`
- `--quantization autoround`
- `--gpu-memory-utilization 0.75`
- `--max-model-len 4096`
- `--enforce-eager`
- `--trust-remote-code`

这些参数与作者在部署试错过程中的重点经验一致：量化、显存利用率控制、上下文长度控制，以及在资源受限场景下关闭 CUDA Graph 来降低显存压力。相关试错和经验总结在上传的部署记录中有详细笔记。

### 8.3 启动 FastAPI

```bash
./scripts/start_fastapi.sh
```

脚本核心逻辑：

- 自动加载 conda
- 激活 `vllm-debug`
- 进入 `fastapi_server`
- 以 `0.0.0.0:9000` 启动 Uvicorn

### 8.4 命令行测试

```bash
./scripts/test_curl.sh
```

---

## 9. 访问方式

### 9.1 电脑本机访问

FastAPI 根接口：

```text
http://127.0.0.1:9000/
```

健康检查：

```text
http://127.0.0.1:9000/health
```

前端演示页：

```text
http://127.0.0.1:9000/web/index.html
```

### 9.2 手机浏览器访问

先获取电脑局域网 IP，例如：

```text
192.168.xxx.xxx
```

然后手机浏览器访问：

```text
http://192.168.xxx.xxx:9000/web/index.html
```

如果前端页面能打开，但接口请求失败，优先检查：

1. FastAPI 是否监听 `0.0.0.0`
2. vLLM 是否监听 `0.0.0.0`
3. 局域网与防火墙配置是否正确
4. WSL/Windows 是否需要端口转发

---

## 10. 前端页面说明

页面分为三个区块：

### 文本输入区

- 输入 prompt
- 调用 `/api/chat/text`
- 显示模型回答

### 文件输入区

- 上传 `.txt / .md / .json / .csv`
- 浏览器读取文本内容
- 调用 `/api/chat/file`
- 输出模型总结或问答结果

### 图片输入区

- 支持手机后摄拍照：`capture="environment"`
- 支持图片预览
- 浏览器压缩后转 base64
- 调用 `/api/chat/image`

另外，页面支持：

- Markdown 渲染
- 数学公式渲染
- 流式打字机效果

---

## 11. 已知限制

当前版本是演示的工程样例，不是完整生产系统，因此存在一些有意保留的简化：

1. **文件理解仅处理文本类文件**
   - 不支持 PDF / Word 直接解析
   - 不支持超长文件的完整分块处理

2. **文件内容有截断**
   - 当前后端默认只取前 6000 字符

3. **图片能力取决于底层模型**
   - 如果当前加载的是纯文本模型，则图片接口即便形式正确，也无法真正看图

4. **无持久化会话**
   - 当前版本不保存聊天历史

5. **无鉴权**
   - 当前版本主要用于本地实验和演示

---

## 12. 可扩展方向

### 工程方向

- 增加日志与请求追踪
- 增加异常处理与统一错误码
- 增加配置文件管理
- 增加 Docker 化部署
- 增加 Nginx 反向代理
- 接入 GitHub Actions

### 推理方向

- 尝试更大模型或多模态模型
- 对比不同量化方式的吞吐与延迟
- 记录 TPS / 首 token 延迟 / 并发性能
- 对比 vLLM、LMDeploy 等不同框架

### 产品方向

- 继续开发安卓 App
- 增加聊天记录
- 增加“拍照即问”模式
- 增加文件多轮问答

---

## 13. 总结

> 基于 vLLM、FastAPI 与 OpenAI 兼容接口实现本地大模型推理服务，设计文本问答、文件理解、图片理解三类 REST API；支持浏览器端图片压缩、流式输出与手机局域网访问，完成从模型启动、服务封装到前端演示的完整链路搭建。

对于部署和推理工程：

> 在消费级 GPU 环境下完成量化模型本地部署与接口封装，具备将模型能力从“能跑”整理为“可演示、可复现、可扩展”的工程实践经验。

---

## 14. 相关学习背景说明

这个项目不是孤立完成的，它是整条“推理加速方向的大模型部署工程师”学习路径中的一个阶段成果。上传的部署学习记录中，前面先从 vLLM 基线部署、量化、显存限制、框架差异、接口调试、手机网页联通等环节逐步推进。

因此，项目价值不只在于“能跑”，更在于它正好处在“从命令行部署 -> API 服务化 -> 多端访问 -> 后续 App 接入”的关键中间层。

---

## 15. 说明

本项目定位为学习型工程样例，重点展示：

- 模型部署
- 接口封装
- 服务联调
- 手机端访问验证

