# -*- Coding: UTF-8 -*-
# pa_豆瓣影评.py
# @作者 giao者
# @创建日期 2021-03-03T18:48:20.269Z+08:00
# @最后修改日期 2021-03-05T11:16:37.468Z+08:00
# @代码说明
#

# 取多页数据：
#  1.打开多个页面，根据他们https网站找规律
#  2.分析’后页‘按钮的网站类型，找规律

# 可优化之处：
# 1.暂时只支持真实存在的作品且为排名第一（比如搜索her有多个结果，但只能取出来第一个，可以试着增加让用户自己选择的权利），
# 异常处理不给力
# 2.词云轮廓待更新
# 3.优化GUI来把它做得像软件,怎么不不需终端也可加入停词和弹出词云图
# 4.webdriver访问服务器总是异常
# 5.输入以及后续识别所需的大小写转换
import requests
import parsel
import jieba
import wordcloud
import imageio
from selenium import webdriver
import wordcloud
import jieba  #中文分词
import matplotlib.pyplot as plt
import mplcyberpunk
from lxml import etree

current_stopwords = set()
# work_name = input('请输入你想搜索的书籍或电影或音乐：')
work_name = ''


# 输入对于当前work_name的特殊停用词
def input_stopwords():

    this_current_stopwords = set()
    flag = True
    while flag:
        item = input('请输入词云屏蔽词，否则输入q：')
        if item == 'q':
            flag = False
        else:
            this_current_stopwords.add(item)
    return this_current_stopwords


def get_work_href_included_id(work_name):
    url = 'https://www.douban.com/search?q=' + work_name
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'
    }
    response = requests.get(url=url, headers=headers)
    # print('response.text is \n\n')
    # print(response.text)
    res_html = etree.HTML(response.text)
    href_included_id_list = res_html.xpath(
        '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/@href'
    )
    href_included_id = 'not found'

    for item in href_included_id_list:
        href_included_id = item
        break
    # print('work_name is ', work_name)
    # print('href_included_id is ', href_included_id)
    return href_included_id


def get_comments_list(work_href):
    if work_href != 'not found':
        page_count = 0
        for page in range(0, 481, 20):
            page_count += 1
            print(
                f'-------------------正在爬取第{page_count}页的数据--------------------'
            )
            url = f'{work_href}/comments?start={page}&limit=20&status=P&sort=new_score'
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'
            }

            response = requests.get(url=url, headers=headers)
            html_data = response.text

            selector = parsel.Selector(
                html_data)  # 转换数据类型 -->xpath 过时：lxml bs4
            comments_list = selector.xpath(
                '//span[@class="short"]/text()').getall()  #getall()取数据

            with open('spider/爬取豆瓣评论做词云图/' + work_name + '_短评.txt',
                      mode='a+',
                      encoding='utf-8') as f:

                for comment in comments_list:
                    # print(comment)
                    f.write(comment.replace('\n', ''))
                    f.write('\n')
                    f.write('\n')
        return comments_list
    else:
        with open('spider/爬取豆瓣评论做词云图/' + work_name + '_短评.txt',
                  mode='a+',
                  encoding='utf-8') as f:
            f.write('not found')
        return ['not found']


"""制作词云图"""


def make_wordcloud_pic(comments_list):
    with open('spider/爬取豆瓣评论做词云图/' + work_name + '_短评.txt',
              mode='r',
              encoding='utf-8') as f:

        txt = f.read()
    if txt == 'not found':
        txt_list_to_string = 'not found'

    else:
        # 中文分词
        txt_list = jieba.lcut(txt)
        # print('中文分词后的结果', txt_list)
        """
        这里join的参数为一个空格，则输出词云图中只有词语。
        若参数为空，则输出词云图有词和句子（但是句子有重复的
        """
        txt_list_to_string = ' '.join(txt_list)
        # print('合并之后的字符串', string1)

    img = imageio.imread('spider/爬取豆瓣评论做词云图/词云轮廓.png')  #词云图的轮廓（待扣）
    """
    如果不扣图的话就不会识别轮廓，整张图片都是词云
    如果扣的话，词语就会按扣除的轮廓排布
    """

    wc = wordcloud.WordCloud(
        # 长宽可以自己想办法从图片提取吗
        width=400,
        height=200,
        background_color='black',
        font_path='msyh.ttc',  # 微软雅黑（系统自带
        mask=img,  # 词云图所用的图片
        scale=10,  #字体大小
        stopwords=set([
            line.strip() for line in open('spider/爬取豆瓣评论做词云图/cn_stopwords.txt',
                                          mode='r',
                                          encoding='utf-8').readlines()
        ]) | current_stopwords  # 停用词即没用的（虚词等）
    )

    # 给词云图输入文字
    wc.generate(txt_list_to_string)

    # 添加赛博朋克风格
    plt.style.use("cyberpunk")
    mplcyberpunk.add_glow_effects()

    # 保存云图
    wc.to_file('spider/爬取豆瓣评论做词云图/' + work_name + '_短评_词云.png')
    return 0


def main(name):
    global work_name
    work_name = str(name)
    # print('work_name in pa_豆瓣.py is ', work_name)
    current_stopwords = input_stopwords()
    work_href = get_work_href_included_id(work_name)
    work_comments_list = get_comments_list(work_href)
    make_wordcloud_pic(work_comments_list)
    return 0
