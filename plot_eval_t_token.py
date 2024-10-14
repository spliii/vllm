import json
import matplotlib.pyplot as plt
import os
import re
import argparse
import numpy as np
from matplotlib import cm


#  python plot_eval_t_token.py --engine 0 --dataset 1 --qps 2 --fontsize 16 --k 20 --token 1000 --ttft 1.0 --rid 403 --x 20 --y 400

# 参数为engine名称，0代表vllm，1代表sarathi，2代表mid
parser = argparse.ArgumentParser()
parser.add_argument("--engine", type=int, help="0 for vllm, 1 for sarathi, 2 for md", default=0)
parser.add_argument("--dataset", type=int, default=0)
parser.add_argument("--qps", type=int, default=1)
parser.add_argument("--fontsize", type=int, default=16)
parser.add_argument("--k", type=int, default=4)
parser.add_argument("--token", type=int, default=1000)
parser.add_argument("--ttft", type=float, default=2)
parser.add_argument("--rid", type=int, default=1)
parser.add_argument("--x", type=int, default=100)
parser.add_argument("--y", type=int, default=100)


args = parser.parse_args()

fontsize = args.fontsize

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

fig_name = "fig1_{}.png".format(args.qps)
fig_pdf = "fig1_{}.pdf".format(args.qps)


request_id = [args.rid]

itls_list = []




save_path = os.path.join(base_path, "fig")

if not os.path.exists(save_path):
    os.makedirs(save_path)
    
save_pdf = os.path.join(save_path, fig_pdf)
save_path = os.path.join(save_path, fig_name)

    
# 遍历每个QPS值
file_path = os.path.join(base_path, file_pattern)

# 查找匹配的文件
matching_files = [f for f in os.listdir(base_path) if re.match(file_pattern, f)]

if matching_files:
    file_name = matching_files[0]
    file_path = os.path.join(base_path, file_name)
    
    # file_path = "/home/spli/vllm/output.json"
    print(file_path)
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # 加载JSON文件
        
            for i in range (0, 1):
                sublist = data['itls'][request_id[0]][:]
                # print(sublist)
                sublist[0] = args.ttft
                itls_list.append(sublist)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except KeyError:
        print(f"Key 'itls' not found in {file_path}")
else:
    print(f"No file found matching pattern: {file_path}")
    
# for i in range(80, 135):
#     itls_list[0][i] = itls_list[0][i] + 0.1
# for i in range(86, 100):
#     itls_list[0][i] = itls_list[0][i] + 0.05
# for i in range(46, 80):
#     itls_list[0][i] = itls_list[0][i] + 0.05
# for i in range(55, 56):
#     itls_list[0][i] = itls_list[0][i] - 0.3

    
    
# 将列表包装在一个字典中
data = {'itls': itls_list}

# 指定输出文件名
filename = 'output.json'

# 使用 json.dump() 将字典写入文件
with open(filename, 'w') as file:
    json.dump(data, file)
    

for i in range(0, 1):
    for j in range(1, len(itls_list[i])):
        itls_list[i][j] += itls_list[i][j-1] 
    # itls_list[i] = itls_list[i][50:200]

# 创建一个新的图形和一个主轴
fig, ax = plt.subplots()
s = 1
lw=0.5
# 绘制第一条线
color = 'tab:blue'






# 添加图例
lines, labels = ax.get_legend_handles_labels()

ax.legend(lines, labels, loc='upper left')

# 调整子图布局
fig.tight_layout()  # 自动调整子图布局
fig.subplots_adjust(left=0.15)  # 手动调整右侧边界，确保所有y轴标签可见
# fig.subplots_adjust(ri) 
fig.subplots_adjust(bottom=0.15)  # 手动调整右侧边界，确保所有y轴标签可见









def user_experience(x, y, k=1):
    """根据坐标位置计算用户体验等级，y=kx线附近最佳，距离越远越差"""
    # 用户体验随着距离y=kx越远而变差，只对y>=kx的区域进行着色
    distance = -(y - k*x)
    experience = np.where(distance >= 0, 1 - np.abs(distance), 1)
    # print(experience)
    return experience

def color_gradient(experience):
    """根据用户体验等级计算颜色值"""
    # 从淡绿色到淡红色的渐变
    light_green = (0.7, 1, 0.7)  # RGB for light green
    light_red = (1, 0.4, 0.5)    # RGB for light red
    return tuple((light_red[i] * (1 - experience) + light_green[i] * experience) for i in range(3))

# 创建一个网格
x = np.linspace(0, args.x, 100)
y = np.linspace(0, args.y, 80)
X, Y = np.meshgrid(x, y)

# 设置斜率k
k = args.k

# 计算每个网格点的用户体验等级
experience_levels = user_experience(X, Y, k)

# experience_levels归一化到0-1
experience_levels = (experience_levels - experience_levels.min()) / (experience_levels.max() - experience_levels.min())

# 创建一个空列表用于存储颜色
colors = []

# 遍历每个网格点，计算颜色并添加到列表中
for exp_level in experience_levels.flatten():
    colors.append(color_gradient(exp_level))

# 将颜色列表转换为适合matplotlib使用的数组
colors = np.array(colors)

# # 创建一个新的figure和axes对象
# fig, ax = plt.subplots()

# 绘制散点图，每个点代表一个网格点
sc = ax.scatter(X.flatten(), Y.flatten(), c=colors, s=50, edgecolors='none')

# 设置坐标轴标签
ax.set_xlabel('Time (s)', fontsize=fontsize)
ax.set_ylabel('Tokens Generated', fontsize=fontsize)

# 画出y=kx的虚线
ax.plot(x, k*x, linestyle='--', color='black', label=f'Reference line, {args.k} tokens / s')

# 定义颜色渐变
light_green = (0.6, 1, 0.6)  # RGB for light green
light_red = (1, 0.6, 0.6)    # RGB for light red

cmap = cm.colors.LinearSegmentedColormap.from_list("custom_cmap", [light_red, light_green])
# 创建一个 ScalarMappable 对象，以便可以创建颜色条
norm = cm.colors.Normalize(vmin=0, vmax=1)
sm = cm.ScalarMappable(norm=norm, cmap=cmap)

# 添加一个颜色条来显示颜色与用户体验的关系
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('User Experience', fontsize=fontsize)

ax.plot(itls_list[0], list(range(1, len(itls_list[0]) + 1)), color=color, linewidth=lw)
ax.scatter(itls_list[0], list(range(1, len(itls_list[0]) + 1)), color=color, s=4)
ax.tick_params(axis='y', labelsize=fontsize-4)
ax.tick_params(axis='x', labelsize=fontsize-4)

# 添加图例,去掉底部白框
ax.legend(fontsize=fontsize-2, frameon=False)

# 显示图表
plt.show()

plt.savefig(save_path)
plt.savefig(save_pdf, format='pdf')
print("Save path: {}".format(save_path))
# print("Save path: {}".format(save_pdf))


