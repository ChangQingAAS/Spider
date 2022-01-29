file = open("../data/testcsv.csv", 'r', encoding='gbk')
while True:
    # 依次读入文件的每一行
    line = file.readline()
    # 如果读到文件末尾，则退出
    if not line:
        break
    # 先去除每行的前后的空格和回车换行符（\n），
# 然后使用逗号（','）拆分每行字符串
    words = line.strip().split(',')
    # 将字符串形式的价格数据转换为小数类型
    price = float(words[1])
    # 判断价格区间，并输出对应价格区间的数量为1
    if price > 0 and price < 1000:
        print('%s\t%s' % ("0~1000", 1))
    elif price < 2000:
        print('%s\t%s' % ("1000~2000", 1))
    elif price < 3000:
        print('%s\t%s' % ("2000~3000", 1))
    elif price < 4000:
        print('%s\t%s' % ("3000~4000", 1))
    else:
        print('%s\t%s' % ("4000~", 1))
