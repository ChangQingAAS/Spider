file = open("../data/words.txt", 'r', encoding='utf-8')
while True:
    # 依次读入文件的每一行
    line = file.readline()
    # 如果读到文件末尾，则退出
    if not line:
        break
    # 使用空格拆分每一行中每个单词
    words = line.split()
    # 输出每个单词对应一个数字 1
    for word in words:
        print('%s\t%s' % (word, 1))