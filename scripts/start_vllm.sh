#!/bin/bash
# chmod +x /home/zxy/codes/test_code/scripts/start_vllm.sh
set -e

# 自动获取 conda 的基础路径并初始化 conda
source "$(conda info --base)/etc/profile.d/conda.sh"

# 现在可以正常激活环境了
conda activate vllm-debug

vllm serve /home/zxy/codes/models/Qwen3.5-0.8B-int4-AutoRound \
  --host 0.0.0.0 \
  --port 8001 \
  --served-model-name qwen3.5-int4 \
  --quantization autoround \
  --gpu-memory-utilization 0.75 \
  --max-model-len 4096 \
  --tensor-parallel-size 1 \
  --disable-frontend-multiprocessing \
  --enforce-eager \
  --trust-remote-code \
  --allowed-origins '["*"]'

# # 【或者直接使用 conda run 指定环境执行 vllm 命令，--no-capture-output 用于实时打印日志】
# conda run -n vllm-debug --no-capture-output vllm serve /home/zxy/codes/models/Qwen3.5-0.8B-int4-AutoRound \
#   --host 0.0.0.0 \
#   --port 8001 \
#   --served-model-name qwen3.5-int4 \
#   --quantization autoround \
#   --gpu-memory-utilization 0.75 \
#   --max-model-len 4096 \
#   --tensor-parallel-size 1 \
#   --disable-frontend-multiprocessing \
#   --enforce-eager \
#   --trust-remote-code \
#   --allowed-origins '["*"]'