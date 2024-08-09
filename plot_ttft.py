import json
import matplotlib.pyplot as plt
import os
import re

# # 定义文件路径和QPS值范围
base_path = "/home/spli/vllm/outputs_script/vllm"
# base_path = "/home/spli/vllm/outputs_script/sarathi"

# base_path = "/home/spli/vllm/outputs_script_mistral/vllm"
# base_path = "/home/spli/vllm/outputs_script_mistral/sarathi"

# file_pattern = "{}.0qps-500-0802-*"
# file_pattern = "{}\.0qps-500.*0808.*"
file_pattern = "{}\.0qps-.*-0808.*"

qps_values = range(1, 21)  # [ , )
# fig_name = "qwen2_500_sharegpt_gpt4_sarathi_1_20_0808.png"
fig_name = "qwen2_500_random_long_2000_400_vllm_1_20_0808.png"

# fig_name = "test_0807_mid.png"

# fig_name = "mistral_500_sharegpt_gpt4_vllm_1_12.png"


# 创建空列表来存储QPS和平均TTFT值
qps_list = []
request_throughput_list = []
mean_ttft_list = []
mean_tpot_list = []
mean_itl_list = []
p99_itl_ms_list = []

save_path = os.path.join(base_path, "fig")

if not os.path.exists(save_path):
    os.makedirs(save_path)
    
save_path = os.path.join(save_path, fig_name)
    
# 遍历每个QPS值
for qps in qps_values:
    file_name_pattern = file_pattern.format(qps)
    file_path = os.path.join(base_path, file_name_pattern)
    
    # 查找匹配的文件
    matching_files = [f for f in os.listdir(base_path) if re.match(file_name_pattern, f)]
    
    if matching_files:
        file_name = matching_files[0]
        file_path = os.path.join(base_path, file_name)
        print(file_name)
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)  # 加载JSON文件
                request_throughput = data['request_throughput']
                mean_ttft = data['mean_ttft_ms']  # 提取mean_ttft_ms
                mean_tpot = data['mean_tpot_ms']
                mean_itl = data['mean_itl_ms']
                p99_itl_ms = data['p99_itl_ms']
                qps_list.append(qps)
                request_throughput_list.append(request_throughput)
                mean_ttft_list.append(mean_ttft)
                mean_tpot_list.append(mean_tpot)
                mean_itl_list.append(mean_itl)
                p99_itl_ms_list.append(p99_itl_ms)
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
ax1.set_ylabel('Request Throughput', color=color)
ax1.plot(qps_list, request_throughput_list, color=color, label='Request Throughput')
ax1.tick_params(axis='y', labelcolor=color)

# 添加数据点的标注
for qps, throughput in zip(qps_list, request_throughput_list):
    ax1.annotate(f'{throughput:.2f}',  # 文本内容
                 xy=(qps, throughput),  # 数据点位置
                 textcoords="offset points",  # 如何解释xytext
                 xytext=(0, 10),  # 相对于数据点的偏移量
                 ha='center',
                 fontsize=8)  # 水平对齐方式
    ax1.scatter(qps, throughput, color='red', s=4)  # 添加红色散点标记

# 创建第二个轴
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Mean TTFT', color=color)
ax2.plot(qps_list, mean_ttft_list, color=color, linestyle='--', label='Mean TTFT')
ax2.tick_params(axis='y', labelcolor=color)

# 创建第三个轴
ax3 = ax1.twinx()
color = 'tab:green'
ax3.spines["right"].set_position(("axes", 1.1))  # 将第三个轴移动到右侧更远的位置
ax3.set_ylabel('Mean TPOT', color=color)
ax3.plot(qps_list, mean_tpot_list, color=color, linestyle='-.', label='Mean TPOT')
ax3.tick_params(axis='y', labelcolor=color)

# 创建第四个轴
ax4 = ax1.twinx()
color = 'tab:brown'
ax4.spines["right"].set_position(("axes", 1.2))  # 将第四个轴移动到右侧更远的位置
ax4.set_ylabel('Mean ITL', color=color)
ax4.plot(qps_list, mean_itl_list, color=color, linestyle=':', label='Mean ITL')
ax4.tick_params(axis='y', labelcolor=color)

# 创建第四个轴
color = 'tab:brown'
ax4.spines["right"].set_position(("axes", 1.2))  # 将第四个轴移动到右侧更远的位置
ax4.set_ylabel('P99 itls', color=color)
ax4.plot(qps_list, p99_itl_ms_list, color=color, linestyle='--', label='P99 ITL')
ax4.tick_params(axis='y', labelcolor=color)

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
lines4, labels4 = ax4.get_legend_handles_labels()
# lines5, labels5 = ax5.get_legend_handles_labels()
ax1.legend(lines + lines2 + lines3 + lines4, labels + labels2 + labels3 + labels4, loc='lower right')

# 调整子图布局
fig.tight_layout()  # 自动调整子图布局
fig.subplots_adjust(right=0.8)  # 手动调整右侧边界，确保所有y轴标签可见

plt.savefig(save_path)