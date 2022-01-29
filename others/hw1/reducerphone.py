import sys
import csv

# newline=''意思是每行信息输出后不产生额外的换行字符
output_csv_file = open('../data/output.csv', 'w', newline='')
# 获取输出文件的写指针对象
csv_writer = csv.writer(output_csv_file)
# 输出 csv 文件的表头信息
csv_writer.writerow(['价格区间', '数量'])
# 声明并初始化保存价格区间信息的变量 current_price_interval
current_price_interval = None
# 声明并初始化保存计数每个价格区间中手机数量的变量 current_count
current_count = 0
# 声明保存当前价格区间信息的变量 price_interval
price_interval = None
# 从标准输入获取输入一行数据
for line in sys.stdin:
    # 去除该行数据前后的空格和回车换行符（\n）
    line = line.strip()
    # 使用制表符拆分每行数据，获取当前价格区间信息和手机计数值，分别放入 price_interval, count 变量中
    price_interval, count = line.split('\t')
    try:
        # 获取手机的计数值的整数形式数值
        count = int(count)
    except ValueError:  # count如果不是数字的话，直接忽略掉
        continue
    # 如果连续两次的价格区间相同，则累加手机计数
    # 此种情况，对应非第一次读入相同价格区间的信息
    if current_price_interval == price_interval:
        current_count += count
    else:
        # 此种情况对应读入一个新的价格区间的情况
        # 此时需要将前一次的价格区间段的信息（手机计数信息）输出
        # 如果当前价格区间信息不为空
        if current_price_interval:
            # 打印输出（上一次）价格区间信息和该价格区间的手机计数信息
            print("%s,%s" % (current_price_interval, current_count))
            # 将当前（其实是上一次）价格区间信息和该价格区间的手机计数信息存入列表 list 中
            list = []
            list.append(current_price_interval)
            list.append(current_count)
            # 将保存当前（其实是上一次）价格区间信息和该价格区间的手机计数信息的列表 list 写入 csv 文件中
            csv_writer.writerow(list)
        # 令 current_count 和 current_price_interval 为新的手机价格区间信息和手机计数信息
        current_price_interval = price_interval
        current_count = count

# 最后输出最后一个手机价格区间计数统计信息
if price_interval == current_price_interval:
    print("%s,%s" % (current_price_interval, current_count))
    # 将最后一个手机价格区间计数统计信息存入列表 list 中
    list = []
    list.append(current_price_interval)
    list.append(current_count)
    # 将保存最后一个价格区间信息和该价格区间的手机计数信息的列表 list 写入 csv 文件中
    csv_writer.writerow(list)
