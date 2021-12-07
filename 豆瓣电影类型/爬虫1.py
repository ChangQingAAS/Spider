import random
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


# 得到所有ip
def get_proxies():
    with open('proxies.txt', 'r') as f:
        result = f.readlines()  # 读取所有行并返回列表
    proxy_ip = random.choice(result)[:-1]  # 获取了所有代理IP
    L = proxy_ip.split(':')
    proxy_ip = {
        'http': 'http://{}:{}'.format(L[0], L[1]),
        'https': 'https://{}:{}'.format(L[0], L[1])
    }
    return proxy_ip


use_agent = '''Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Mobile Safari/537.36'''
cookies = '''bid=aRWCx_o9ovw; douban-fav-remind=1; ll="108289"; __yadk_uid=oIRENnbKBZrrPUpn0dHiwYH4mWau0ZKe; _vwo_uuid_v2=D8CDE504B20AE50F2CB1A7AFCB376310D|122bd69a044b25a07a2c0c97b17c8115; __gads=ID=f9cdd590f3772e2b:T=1588089186:S=ALNI_Ma4DGpKZD3qkgFNFrBeUPNUdXOJvg; __utmz=30149280.1588571318.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1588571318.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ct=y; _ga=GA1.2.1212864927.1573785067; _gid=GA1.2.49643196.1588652735; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588660774%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DI4PdG-59niXGFx0u9MqfavlHjlV3QSLslvgdsY_rnOMGlrjkysTPpcQ09iI5qlah%26wd%3D%26eqid%3Df3567af9000ef4b2000000025eafacb1%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1212864927.1573785067.1588658332.1588660774.9; __utmb=30149280.0.10.1588660774; __utma=223695111.439676028.1588089181.1588658332.1588660774.8; __utmb=223695111.0.10.1588660774; _pk_id.100001.4cf6=8045bf86c0e7354d.1588089181.8.1588661147.1588658332.; __utmc=30149280; __utmc=223695111'''
headers = {
    'Cookie': cookies,
    'User-Agent': use_agent,
    'Referer': 'https://movie.douban.com/subject/26752088/comments?status=P',
    'Connection': 'keep-alive'
}

for i in range(0, 10):
    all_movie_data = []
    url = "https://movie.douban.com/top250?start=" + (str(i * 25))
    # 获取网页
    response = requests.get(url, headers=headers)
    # response = requests.get(url, headers=headers, proxies=get_proxies(), timeout=10)

    # 解析网页
    soup = BeautifulSoup(response.text, "html.parser")
    movie_list = soup.find_all('div', class_='info')
    print("\n" + str(i + 1) + " 页:\n")
    # 遍历网页信息
    for movie_information in movie_list:
        data = []
        try:
            m_name = movie_information.find(name='span', class_='title').text
            m_score = movie_information.find(name='span',
                                             class_='rating_num').text
            m_url = movie_information.find(name='a')
            match_re = re.compile('href="https://.*')
            m_url = match_re.findall(str(m_url))[0][6:-2]

            data.append(m_name)
            data.append(m_score)
            data.append(m_url)

            print(m_name + "            " + m_score)
            print(m_url)

            # response = requests.get(m_url, headers=headers, proxies=get_proxies(), timeout=10)
            response = requests.get(m_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # information = soup.find('div', attrs={'class': 'sub-meta'})
            informations = soup.find('div', attrs={'id': 'info'})
            informations = informations.text.split('\n')
            for info in informations:
                if "类型" in info:
                    print(info.split(':')[1])
                    data.append(info.split(':')[1])
                if '日期' in info:
                    print(info.split(':')[1])
                    match_time = re.compile('\d.{9}')
                    start_time = match_time.findall(str(info.split(':')[1]))[0]
                    print(start_time)
                    data.append(start_time)
                if '地区' in info:
                    print(info.split(':')[1])
                    # information = str(information.text).replace(' ', '').replace('\n', '')
                    data.append(info.split(':')[1])
                # information = soup.find('div', attrs={'class': 'sub-meta'})
            content = soup.find('span', attrs={'property': 'v:summary'})
            content = content.text.replace(' ', '')
            print(content)
            data.append(content)

            all_movie_data.append(data)
            time.sleep(5)
        except:
            pass

    pd.DataFrame(all_movie_data).to_excel('./data/第' + str(i) + '页.xlsx',
                                          encoding='utf-8')
