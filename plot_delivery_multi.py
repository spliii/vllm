import json
import matplotlib.pyplot as plt
import os
import re
import argparse

# python plot_delivery_multi.py --engine 0 --dataset 0 --qps 1 --rid 1

# 参数为engine名称，0代表vllm，1代表sarathi，2代表mid
parser = argparse.ArgumentParser()
parser.add_argument("--engine", type=int, help="0 for vllm, 1 for sarathi, 2 for mid", default=0)
parser.add_argument("--dataset", type=int, default=0)
parser.add_argument("--qps", type=int, default=1)
parser.add_argument("--rid", type=int, default=1)

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
    engine0 = "vllm"
    engine1 = "sarathi"
elif args.engine == 1:
    engine0 = "vllm"
    engine1 = "mid"
elif args.engine == 2:
    engine0 = "sarathi"
    engine1 = "mid"


base_path0 = "/home/spli/vllm/{}/{}".format(dataset, engine0)
base_path1 = "/home/spli/vllm/{}/{}".format(dataset, engine1)

fig_name = "delivery_multi_0808_{}_{}.png".format(engine0, engine1)

request_id = [args.rid]

itls_list = []

save_path0 = os.path.join(base_path0, "fig")
save_path1 = os.path.join(base_path1, "fig")

if not os.path.exists(save_path0):
    os.makedirs(save_path0)
if not os.path.exists(save_path1):
    os.makedirs(save_path1)

    
save_path0 = os.path.join(save_path0, fig_name)
save_path1 = os.path.join(save_path1, fig_name)
    
# 遍历每个QPS值
file_path0 = os.path.join(base_path0, file_pattern)
file_path1 = os.path.join(base_path0, file_pattern)

# 查找匹配的文件
matching_files0 = [f for f in os.listdir(base_path0) if re.match(file_pattern, f)]
matching_files1 = [f for f in os.listdir(base_path1) if re.match(file_pattern, f)]

if matching_files0 and matching_files1:
    file_name0 = matching_files0[0]
    file_path0 = os.path.join(base_path0, file_name0)
    print(file_path0)
    file_name1 = matching_files1[0]
    file_path1 = os.path.join(base_path1, file_name1)
    print(file_path1)

    with open(file_path0, 'r') as file:
        data = json.load(file)  # 加载JSON文件
    
        for i in range (0, 1):
            sublist = data['itls'][request_id[i]]
            itls_list.append(sublist)
    with open(file_path1, 'r') as file:
        data = json.load(file)  # 加载JSON文件
    
        for i in range (0, 1):
            sublist = data['itls'][request_id[i]]
            itls_list.append(sublist)

else:
    print(f"No file found matching pattern: {file_path}")



for i in range(0, 2):
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
ax1.plot(list(range(1, len(itls_list[0]) + 1)),itls_list[0], color=color, label=engine0, linewidth=lw)
ax1.scatter(list(range(1, len(itls_list[0]) + 1)), itls_list[0], color=color, s=s)
ax1.tick_params(axis='y', labelcolor=color)

color = 'tab:blue'
ax1.plot(list(range(1, len(itls_list[1]) + 1)), itls_list[1], color=color, label=engine1, linewidth=lw)
ax1.scatter(list(range(1, len(itls_list[1]) + 1)),  itls_list[1], color=color, s=s)


# 添加图例
lines, labels = ax1.get_legend_handles_labels()
ax1.legend(lines, labels, loc='upper left')

# 调整子图布局
fig.tight_layout()  # 自动调整子图布局
fig.subplots_adjust(right=0.8)  # 手动调整右侧边界，确保所有y轴标签可见

plt.savefig(save_path0)
plt.savefig(save_path1)
print("Save path: {}".format(save_path0))