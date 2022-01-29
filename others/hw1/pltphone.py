import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

df = pd.read_csv('../data/output.csv', encoding='gbk')
# 获取 csv 文件中“价格区间”列的数据
x = df['价格区间'].tolist()
print(x)
# 获取获取 csv 文件中手机计数信息“数量”列的数据
y = df['数量'].tolist()
# 指定直方图的x轴、y轴的数据，宽度为0.5，颜色为红色
a = plt.bar(x, y, width=0.5, color='red')
# 指定默认的中文字体
mpl.rcParams['font.sans-serif'] = ['FangSong']
# 解决保存图像负号'-'显示为乱码的问题
mpl.rcParams['axes.unicode_minus'] = False
# 设置x轴、y轴的显示信息
plt.xlabel('手机价格区间')
plt.ylabel('数量')
# 设置右上角显示图示信息
plt.legend(['手机价格区间统计'], loc='upper right')
# 绘制可视化直方图
plt.show()
