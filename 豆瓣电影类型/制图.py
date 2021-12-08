import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置汉字格式
# sans-serif就是无衬线字体，是一种通用字体族。
# 常见的无衬线字体有 Trebuchet MS, Tahoma, Verdana, Arial, Helvetica,SimHei 中文的幼圆、隶书等等
plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

Data = pd.read_excel('./data/0.xlsx')
map_num = {}
for data in Data.values:
    all = str(data[4]).replace(' ', '').split('/')
    for item in all:
        if item not in map_num:
            map_num[item] = 1
        else:
            map_num[item] += 1
print(map_num)
region = []
num = []
for k, v in map_num.items():
    region.append(k)
    num.append(v)

plt.pie(num, labels=region)
plt.title('不同类型优秀电影数量饼状图')
plt.savefig('pie_plot.png', bbox_inches='tight')
plt.show()