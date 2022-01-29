from fontTools.ttLib import TTFont
from math import sqrt
import re
import requests
from bs4 import BeautifulSoup

cookie = '''__mta=219045542.1588042872942.1588697401404.1588724790066.11; _lxsdk_cuid=171bebb082e46-092b205db2c01-39624307-144000-171bebb082fc8; t_lxid=171bebb0848c8-090db35e36898d-39624307-144000-171bebb0848c8-tid; uuid_n_v=v1; uuid=80C9B3E088FC11EABF58AFCA1C6B1860E1E7A3B3B3B94CFC857B2BECD342644F; mojo-uuid=4195bee6651bddb32f364f2b1e43a38e; _lxsdk=80C9B3E088FC11EABF58AFCA1C6B1860E1E7A3B3B3B94CFC857B2BECD342644F; __mta=219045542.1588042872942.1588140325347.1588689380359.9; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _csrf=79112cc18b1809de8acc1e153c7b173e95bd1f036a3cfd3568e1ae7c6276f842; mojo-session-id={"id":"f1ee0d5e396fc431799369a43d64712b","time":1588724789683}; mojo-trace-id=1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1588138901,1588689010,1588689380,1588724790; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1588724790; _lxsdk_s=171e75a2534-6ce-6e7-cdf%7C%7C3'''
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
    'Cookie': cookie
}


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


def toXML():
    # 将woff格式转化成xml格式
    template_font = TTFont('font/font1.woff')
    template_font.saveXML('font/font1.xml')


# 计算两个字符间的平均距离
def DIST(list):
    d = 0
    for point in list:
        x1, x2 = point
        d = d + sqrt(pow(x1[0] - x2[0], 2) + pow(x1[1] - x2[1], 2))
    d = d / len(list)
    return d


# 字体解密
def deciphering(html, template_file, check_file):
    template_data = {
        'uniF7A3': 7,
        'uniE4FC': 3,
        'uniECEF': 1,
        'uniF2DA': 8,
        'uniE2EB': 5,
        'uniE252': 9,
        'uniF793': 4,
        'uniEFB1': 6,
        'uniE1A9': 0,
        'uniE51C': 2
    }

    # 提取网页中被加密的字符
    reg_num = re.compile(r'&#x(.*?);')
    # 提取字符并去重，减少计算量
    encryption_num = set(reg_num.findall(html))

    # 读取模板字体库信息
    template_font = TTFont(template_file)
    template_index = template_font.getGlyphOrder()[2:]
    # 读取新的字体库信息
    target_font = TTFont(check_file)

    # 字体解密
    correct_num = {}
    num = {}
    # 遍历每个要计算的字符
    for item in encryption_num:
        target = target_font['glyf']['uni' + item.upper()].coordinates
        dist_min = 10000  # 随便设，一般最小距离不会大于200
        # 遍历模板每个字符
        for index in template_index:
            template = template_font['glyf'][index].coordinates
            # 因为每个字体库的相同字体，坐标点数量会不一样
            # 所以需要做一个判断，坐标数量相差少于10个，也起到筛选作用
            if abs(len(target) - len(template)) < 10:
                # 对满足条件的字符进行计算
                dist = DIST(list(zip(target, template)))
                # 找出最小平均距离的字符，嗯，答案就是最小的它了
                if dist < dist_min:
                    dist_min = dist
                    num[item] = index
    # 构建两个字体库的新映射
    for index in encryption_num:
        correct_num['&#x' + index + ';'] = template_data[num[index]]
    return correct_num


# 解析页面，提取信息
def bs4Handle(path):
    movie = {}
    with open(path, "r", encoding="utf-8") as fp:
        html = fp.read()
    soup = BeautifulSoup(html, "lxml")
    # 选取所有的简介内容
    movie['title'] = soup.select("h1.name")[0].text
    movie['score'] = soup.select('span.index-left.info-num')[0].text
    movie['number'] = soup.select('span.score-num')[0].text
    movie['box'] = soup.select('div.movie-index-content.box')[0].text
    return movie


font1 = TTFont('font/font1.woff')
font2 = TTFont('font/font2.woff')
# 这个能看他们的坐标数量
test1 = font1['glyf']['uniF7A3'].coordinates
test2 = font2['glyf']['uniE5A4'].coordinates
print(len(test1))
print(len(test2))

if __name__ == '__main__':

    # 活着 ： https://maoyan.com/films/1375
    url = 'https://maoyan.com/films/1375'
    response = requests.get(url, headers=headers)
    html = response.text

    font_url = get_font_url(html)
    save_font(font_url, 'font/fontx.woff')

    correct = deciphering(html, 'font/font1.woff', 'font/fontx.woff')

    for key in correct:
        html = html.replace(key, str(correct[key]))

    # 将已经解密的html文件保存
    with open('data/content.html', "w", encoding="utf-8") as fp:
        fp.write(html)

    # 读出保存的html中的指定信息
    movie = bs4Handle('data/content.html')
    print(movie)