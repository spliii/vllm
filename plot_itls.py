import json
import matplotlib.pyplot as plt
import os
import re

# # 定义文件路径和QPS值范围
# base_path = "/home/spli/vllm/outputs_script_long/sarathi"
# base_path = "/home/spli/vllm/outputs_script/sarathi"
base_path = "/home/spli/vllm/outputs/sarathi"

# base_path = "/home/spli/vllm/outputs_script_mistral/vllm"
# base_path = "/home/spli/vllm/outputs_script_mistral/sarathi"
# /home/spli/vllm/outputs/vllm/random-100.0qps-2-p(2000,10000)-1.0-seed42-0813-142531.json
# file_pattern = "{}.0qps-500-0802-*"
# file_pattern = ".*-15.0qps-500.*0808-1.*"
file_pattern = ".*0813-144.*"

# qps_values = range(3, 6)  # [ , )
# fig_name = "qwen2_500_sharegpt_gpt4_vllm_1_18.png"
fig_name = "itls_0808_15.png"
fig_name = "itls_0813_sarathi.png"

request_id = [1 , 55, 405]
request_id = [0, 1, 0]

# fig_name = "mistral_500_sharegpt_gpt4_vllm_1_12.png"


# 创建空列表来存储QPS和平均TTFT值

itls_list = []

save_path = os.path.join(base_path, "fig")

if not os.path.exists(save_path):
    os.makedirs(save_path)
    
save_path = os.path.join(save_path, fig_name)
    
# 遍历每个QPS值
file_path = os.path.join(base_path, file_pattern)

# 查找匹配的文件
matching_files = [f for f in os.listdir(base_path) if re.match(file_pattern, f)]

if matching_files:
    file_name = matching_files[0]
    file_path = os.path.join(base_path, file_name)
    print(file_path)

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # 加载JSON文件
        
            for i in range (0, 3):
                sublist = data['itls'][request_id[i]][1:]
                itls_list.append(sublist)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except KeyError:
        print(f"Key 'mean_ttft_ms' not found in {file_path}")
else:
    print(f"No file found matching pattern: {file_path}")

# # 绘制QPS-平均TTFT的折线图
# plt.figure(figsize=(10, 5))
# plt.plot(qps_list, mean_ttft_list, marker='o')
# plt.title('QPS - Average TTFT')
# plt.xlabel('QPS')
# plt.ylabel('Average TTFT (ms)')
# plt.grid(True)
# plt.xticks(qps_values)
# plt.savefig(save_path)

# 创建一个新的图形和一个主轴
fig, ax1 = plt.subplots()

# 绘制第一条线
color = 'tab:red'
ax1.set_xlabel('QPS')
ax1.set_ylabel('1', color=color)
ax1.plot(list(range(1, len(itls_list[0]) + 1)), itls_list[0], color=color, label='Request Throughput')
ax1.tick_params(axis='y', labelcolor=color)

# 创建第二个轴
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('50', color=color)
ax2.plot(list(range(1, len(itls_list[1]) + 1)),  itls_list[1], color=color, linestyle='--', label='Mean TTFT')
ax2.tick_params(axis='y', labelcolor=color)

# 创建第三个轴
ax3 = ax1.twinx()
color = 'tab:green'
ax3.spines["right"].set_position(("axes", 1.1))  # 将第三个轴移动到右侧更远的位置
ax3.set_ylabel('100', color=color)
ax3.plot(list(range(1, len(itls_list[2]) + 1)),  itls_list[2], color=color, linestyle='-.', label='Mean TPOT')
ax3.tick_params(axis='y', labelcolor=color)

# # 创建第四个轴
# ax4 = ax1.twinx()
# color = 'tab:orange'
# ax4.spines["right"].set_position(("axes", 1.2))  # 将第四个轴移动到右侧更远的位置
# ax4.set_ylabel('Mean ITL', color=color)
# ax4.plot(qps_list, mean_itl_list, color=color, linestyle=':', label='Mean ITL')
# ax4.tick_params(axis='y', labelcolor=color)

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='upper left')

# 调整子图布局
fig.tight_layout()  # 自动调整子图布局
fig.subplots_adjust(right=0.8)  # 手动调整右侧边界，确保所有y轴标签可见

plt.savefig(save_path)
print(save_path)