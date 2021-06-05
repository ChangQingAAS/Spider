import re
import requests
from selenium import webdriver
import csv
import time
import json
import pandas as pd


def get_data(name, code, page=11):

    df_list = []
    for index in range(1, page):
        url = f'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18305916847893465669_1614240474805&fundCode={code}&pageIndex={index}&pageSize=20&startDate=&endDate=&_=1614240497014'

        headers = {
            # 防盗链 确定来路
            'Referer':
            'http://fundf10.eastmoney.com/jjjz_000001.html',
            # 身份证
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
        }
        # 模拟浏览器发送请求，接收数据
        response = requests.get(url, headers=headers)

        html = response.text
        res = re.findall('\((.*?)\)', html)
        datas = json.loads(res[0])["Data"]["LSJZList"]  # 字典
        # 转成二维表格
        df = pd.DataFrame(datas)
        # with open('spider/天天基金数据.json', mode='a+') as f:
        #     f.write(str(df))
        df_list.append(df)

    df_data = pd.concat(df_list)
    df_data.to_csv(f'spider/天天基金数据/{name}.csv', index=False)


def get_fund_ranking(num):
    base_url = f'https://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-02-25&ed=2021-02-25&qdii=&tabSubtype=,,,,,&pi={num}&pn=50&dx=1&v=0.317351912127922'
    headers = {
        # 防盗链 确定来路
        'Referer':
        'https://fund.eastmoney.com/data/fundranking.html',
        # 身份证
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
    }
    response = requests.get(base_url, headers=headers)
    result = re.findall('"(.*?)"', response.text)
    # print(len(result))
    for i in result:
        code = i.split(',')[0]
        name = i.split(',')[1]
        get_data(name, code)


# get_fund_ranking(2)

# 数据可视化
import matplotlib.pyplot as plt
import mplcyberpunk

plt.style.use("cyberpunk")
plt.plot([])
mplcyberpunk.add_glow_effects()
plt.show()
