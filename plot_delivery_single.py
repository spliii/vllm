import json
import matplotlib.pyplot as plt
import os
import re
import argparse

# python plot_delivery_engine.py --engine 0 --dataset 0 --qps 1

# 参数为engine名称，0代表vllm，1代表sarathi，2代表mid
parser = argparse.ArgumentParser()
parser.add_argument("--engine", type=int, help="0 for vllm, 1 for sarathi, 2 for mid", default=0)
parser.add_argument("--dataset", type=int, default=0)
parser.add_argument("--qps", type=int, default=1)

args = parser.parse_args()

dataset="outputs_script"

if args.dataset == 0:
    dataset = "outputs_script"
    file_pattern = "{}.0qps-500.*0808-.*".format(args.qps)
elif args.dataset == 1:
    dataset = "outputs_script_long"
    file_pattern = "random-{}.0qps-500-p.*0808-.*".format(args.qps)
    
engine = "vllm"

if args.engine == 0:
    engine = "vllm"
elif args.engine == 1:
    engine = "sarathi"
elif args.engine == 2:
    engine = "mid"


base_path = "/home/spli/vllm/{}/{}".format(dataset, engine)

fig_name = "delivery_0808_{}.png".format(args.qps)

request_id = [1 , 55, 405]

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
                sublist = data['itls'][request_id[i]]
                itls_list.append(sublist)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except KeyError:
        print(f"Key 'itls' not found in {file_path}")
else:
    print(f"No file found matching pattern: {file_path}")



for i in range(0, 3):
    for j in range(1, len(itls_list[i])):
        itls_list[i][j] += itls_list[i][j-1] 
    # itls_list[i] = itls_list[i][50:200]

# 创建一个新的图形和一个主轴
fig, ax1 = plt.subplots()
s = 1
lw=0.5
# 绘制第一条线
color = 'tab:red'
ax1.set_xlabel('tokens')
ax1.set_ylabel('1', color=color)
ax1.plot(list(range(1, len(itls_list[0]) + 1)),itls_list[0], color=color, label='1', linewidth=lw)
ax1.scatter(list(range(1, len(itls_list[0]) + 1)), itls_list[0], color=color, s=s)
ax1.tick_params(axis='y', labelcolor=color)

# 创建第二个轴
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('55', color=color)
ax2.plot(list(range(1, len(itls_list[1]) + 1)), itls_list[1], color=color, label='55', linewidth=lw)
ax2.scatter(list(range(1, len(itls_list[1]) + 1)),  itls_list[1], color=color, s=s)
ax2.tick_params(axis='y', labelcolor=color)

# 创建第三个轴
ax3 = ax1.twinx()
color = 'tab:green'
ax3.spines["right"].set_position(("axes", 1.1))  # 将第三个轴移动到右侧更远的位置
ax3.set_ylabel('405', color=color)
ax3.plot(list(range(1, len(itls_list[2]) + 1)), itls_list[2], color=color, label='405', linewidth=lw)
ax3.scatter(list(range(1, len(itls_list[2]) + 1)),  itls_list[2], color=color, s=s)
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
print("Save path: {}".format(save_path))