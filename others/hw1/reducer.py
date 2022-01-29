import sys

current_word = None
current_count = 0
word = None
# 从标准输入获取输入一行数据
for line in sys.stdin:
    # 去除改行数据前后的空格
    line = line.strip()
    # 使用制表符拆分输入
    word, count = line.split('\t')
    try:
        # 获取单词的计数的整数形式数值
        count = int(count)
    except ValueError:  #count如果不是数字的话，直接忽略掉
        continue
    # 如果连续两次的单词相同，则累加单词计数
    if current_word == word:
        current_count += count
    else:
        # 打印输出上一个单词计数统计信息
        if current_word:
            print("%s\t%s" % (current_word, current_count))
        # 令current_count和current_word为新的单词计数信息
        current_count = count
        current_word = word
# 最后输出最后一个单词计数统计信息
if word == current_word:
    print("%s\t%s" % (current_word, current_count))
