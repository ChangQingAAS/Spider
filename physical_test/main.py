import requests

url = f'http://test.tfht.com.cn/Wap/scorelist.aspx?year=2021&actid=1'

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
    'Cookie': '',
    'Referer': 'http://test.tfht.com.cn/Wap/score.aspx?testyear=2021',
    'Connection': 'keep-alive',
    'sec-ch-ua-platform': "Windows",
    'Host': 'test.tfht.com.cn',
}

response = requests.post(url, headers=headers)
response.encoding = 'utf-8'

html = response.text

print(html)

with open("./physical_test/l.html", mode="w+", encoding="utf-8") as f:
    f.write(html)
"""
cookies 不能很好地获取到(有一套计算，还需要知道对应id人的姓名，太费劲了），故此法作废，改用笨拙的webdriver
"""