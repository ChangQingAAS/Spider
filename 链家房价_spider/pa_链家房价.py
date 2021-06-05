# -*- Coding: UTF-8 -*-
# pa_房价.py
# @作者 giao者
# @创建日期 2021-02-25T10:35:39.393Z+08:00
# @最后修改日期 2021-02-25T10:36:39.874Z+08:00
# @代码说明 爬取链家网站的天津房价
#
'''
爬虫的用途：数据分析（数据的预测等），模型训练，行业判断
通用的数据采集：聚焦爬虫（反爬<验证码/ip封锁>

爬虫案例的一般实现步骤：
1.确认数据所在url链接地址；静态网页/动态网页
2.发送制定url地址的请求（html\js\css\
3.数据解析（提取数据
4.数据保存（数据持久化）<数据库，或本地文件>

看不到数据，你又想爬取（渗透、攻击
'''
import requests
import csv
import parsel
import re

with open('spider/链家房价_spider/天津房价.csv',
          mode='a+',
          encoding='utf-8',
          newline='\n') as f:
    csv_write = csv.writer(f)  # 一个写入csv文件类型的对象
    csv_write.writerow(['商品名称', '地址', '介绍', '标签', '总价（万元）', '每平米价格（元）'])

for page in range(1, 101):
    print(f'=====现在正在爬取第{page}页====')
    url = f'https://tj.lianjia.com/ershoufang/pg{page}/'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    }
    response = requests.get(url=url, headers=headers)

    with open('spider/链家房价_spider/天津房价.json', mode='w+',
              encoding='utf-8') as f:
        f.write(response.text)

    html_data = response.text

    # css解析方式
    selector = parsel.Selector(html_data)
    lis = selector.css('.clear.LOGCLICKDATA')

    for li in lis:  # 二次提取
        # 房子标题
        title = li.css('.title a::text').get()
        # 地址
        address = li.css('.positionInfo a::text').getall()  #getall获取所有数据
        address = '- '.join(address)
        # 介绍
        introduce = li.css('.houseInfo::text').get()
        # 关注
        star = li.css('.followInfo::text').get()
        # 标签（vr看房、房本年限）
        tags = li.css('.tag span::text').getall()
        tags = ','.join(tags)
        # 价格
        totalPrice = li.css('.priceInfo .totalPrice span::text').get()
        unitPrice = li.css('.unitPrice span::text').get()
        unitPrice = int(re.findall('单价(.*?)元/平米', unitPrice)[0])

        # print(title, address, introduce, tags, totalPrice, unitlPrice, sep='\n')
        # print("\n")

        with open('spider/链家房价_spider/天津房价.csv',
                  mode='a+',
                  encoding='utf-8',
                  newline='\n') as f:
            csv_write = csv.writer(f)  # 一个写入csv文件类型的对象
            csv_write.writerow(
                [title, address, introduce, tags, totalPrice, unitPrice])
