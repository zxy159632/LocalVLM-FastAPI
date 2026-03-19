#!/bin/bash
# 
set -e
curl http://127.0.0.1:9000/api/chat/text \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "你好，请做个自我介绍"
  }'

# # 【流式,但是未解析】
# set -e
# curl http://127.0.0.1:8001/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "qwen3.5-int4",
#     "messages": [
#         {"role": "user", "content": "你好，请做个自我介绍"}
#     ],
#     "max_tokens": 128,
#     "temperature": 0.7,
#     "stream": true
# }'