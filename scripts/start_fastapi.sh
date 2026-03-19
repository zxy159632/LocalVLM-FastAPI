#!/bin/bash
# chmod +x /home/zxy/codes/test_code/scripts/start_fastapi.sh
set -e

# 自动获取 conda 的基础路径并初始化 conda
source "$(conda info --base)/etc/profile.d/conda.sh"

# 现在可以正常激活环境了
conda activate vllm-debug

cd /home/zxy/codes/test_code/fastapi_server
uvicorn main:app --host 0.0.0.0 --port 9000 --reload