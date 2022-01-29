# author: admin
# time: 2020/5/5 22:55

import re
import requests


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }

# 提取字体库地址
def get_font_url(html):
    reg_url = re.compile(r"url\('(.*?)'\)")
    urls = reg_url.findall(html)
    font_url = 'https:' + urls[2]
    return font_url


# 下载font文件,并保存到本地
# 注意，源文件是 woff格式， 保存的的格式也要是woff格式， 即 xxx.woff
def save_font(url, file_name):
    response = requests.get(url, headers=headers)
    with open(file_name, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
# //vfile.meituan.net/colorstone/8231b633759b748a0ce4671285fda25f2272.woff
# //vfile.meituan.net/colorstone/da582b0146c79c70bb9a3c5712844b032284.woff
# //vfile.meituan.net/colorstone/da582b0146c79c70bb9a3c5712844b032284.woff

    url = 'https://maoyan.com/films/1375'
    response = requests.get(url, headers=headers)
    html = response.text
    font_url = get_font_url(html)
    save_font(font_url, 'font/fontx.woff')
