#!/bin/bash

# 定义基本命令
# base_command="python benchmarks/benchmark_serving.py \
#         --backend vllm \
#         --model /data2/sp/models/Qwen2-7B-Instruct/ --port 8005 \
#         --dataset-name sharegpt \
#         --dataset-path /data2/sp/datasets/sharegpt_gpt4.json \
#         --num-prompts 500 \
#         --save-result --result-dir ./outputs_script/mid"

base_command="python benchmarks/benchmark_serving.py \
        --backend vllm \
        --model /data2/sp/models/Qwen2-7B-Instruct/ --port 8015 \
        --dataset-name random \
        --random-input-len 2000 --random-output-len 400 --random-range-ratio 0.6 --seed 42 \
        --num-prompts 500 \
        --save-result --result-dir ./outputs_script_long/sarathi"

# 循环从1到10
for rate in {11..20}; do
    # 构建完整命令
    full_command="${base_command} --request-rate ${rate}"

    # 执行命令并后台运行
    echo "Executing command: $full_command"
    nohup $full_command &

    # 等待当前命令完成
    wait

    # 输出完成信息
    echo "Completed execution with request-rate ${rate}"
done

echo "All commands have been executed."
