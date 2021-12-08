# 根据豆瓣电影TOP250预测上映电影类型
import os
from urllib import request
from lxml import etree
from collections import Counter  # 计算列表中元素的包
import collections
import re  # 正则表达式包，for cutting the punctuations

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}
all_type = []


def crow(i):
    # 声明要爬取的页面url地址
    url = 'https://movie.douban.com/top250?start=' + str(25 * i)
    # 如果不设置用户代理，因为有的网站有反爬虫的机制，造成418错误
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    # 将头部信息加入到相应的request请求中
    res = request.Request(url, headers=headers)
    html = request.urlopen(res).read().decode('utf-8')
    # 将返回的字符串格式的html代码转换成xpath能处理的对象
    html = etree.HTML(html)
    # 先定位到li标签，datas是一个包含25个li标签的list，就是包含25部电影信息的list
    datas = html.xpath('//ol[@class="grid_view"]/li')
    a = 0
    for data in datas:
        data_title = data.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()')
        data_info = data.xpath('div/div[2]/div[@class="bd"]/p[1]/text()')
        data_quote = data.xpath('div/div[2]/div[@class="bd"]/p[2]/span/text()')
        data_score = data.xpath(
            'div/div[2]/div[@class="bd"]/div/span[@class="rating_num"]/text()')
        data_num = data.xpath('div/div[2]/div[@class="bd"]/div/span[4]/text()')
        movie_type = data_info[1].strip("\n").split('\xa0/\xa0')[2]
        all_type.append(movie_type)
        # 保存电影信息到txt文件
        with open('douban250.txt', 'a', encoding='utf-8') as f:
            f.write("No: " + str(i * 25 + a + 1) + '\n')
            f.write(data_title[0] + '\n')
            f.write(str(data_info[0]).strip() + '\n')
            f.write(str(data_info[1]).strip() + '\n')
            if data_quote:
                f.write(data_quote[0] + '\n')
            f.write(data_score[0] + '\n')
            f.write(data_num[0] + '\n')
            f.write('\n' * 3)
        a += 1


for i in range(10):
    crow(i)

categories = []
for i in range(len(all_type)):
    category = all_type[i].strip("\n").split(' ')
    for j in range(len(category)):
        categories.append(category[j])
# print(categories)

result = Counter(categories)
result_sort = sorted(result.items(), key=lambda x: x[1],
                     reverse=True)  #排序 order descending and by x[1]
result_sort = collections.OrderedDict(result_sort)
print("最受欢迎的电影TOP250类型统计如下：")
x = 1
types = []
for i in result_sort.keys():
    if x == 1:
        x += 1
        continue
    elif x == 7:
        break
    else:
        types.append(str(i).strip("\n"))
        print(str(i).strip("\n") + "," + str(result_sort[i]))
        x += 1
print("由此可以预测2021年可能上映的电影类型为：", end='')
print(",".join(str(i) for i in types))
