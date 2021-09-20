# spider_douban_comments.py
# @created 2021-03-07T15:23:32.377Z+08:00
# @last-modified 2021-09-20T11:19:07.626Z+08:00
#

import requests
import parsel
import jieba
import wordcloud
import imageio
import matplotlib.pyplot as plt
import mplcyberpunk
from lxml import etree
from etc import headers
import re

# 定义一些全局变量
current_stopwords = set()
# work_name = input('请输入你想搜索的书籍或电影或音乐：')
work_name = ''


# 输入对于当前work_name的特殊停用词
def input_stopwords(stopwords):

    # this_current_stopwords = set()
    # flag = True
    # while flag:
    #     item = input('请输入词云屏蔽词，否则输入q：')
    #     if item == 'q':
    #         flag = False
    #     else:
    #         this_current_stopwords.add(item)
    this_current_stopwords = stopwords
    return this_current_stopwords


def get_work_href_included_id(work_name):

    url = 'https://www.douban.com/search?q=' + work_name
    # print("url is ", url)
    response = requests.get(url=url, headers=headers)
    print("response status when get_href ", response)

    res_html = etree.HTML(response.text)
    href_included_id_list = res_html.xpath(
        '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/@onclick'
    )[0]

    find_type = re.compile(r'dou_search_(.*?)\'', re.S)   
    type = re.findall(find_type, href_included_id_list)[0]
    find_sid = re.compile(r'sid: (.*?),', re.S)   
    sid = re.findall(find_sid, href_included_id_list)[0]

    if type == None:
        href_included_id = 'not found'
    else:    
        href_included_id = 'https://' + type + '.douban.com/subject/' + sid  
    
    # print('href_included_id is ', href_included_id)
    return href_included_id


def get_comments_list(work_href):
    if work_href != 'not found':
        page_count = 0
        for page in range(0, 21, 20):
            page_count += 1
            print(
                f'-------------------正在爬取第{page_count}页的数据--------------------'
            )
            url = f'{work_href}/comments?start={page}&limit=20&status=P&sort=new_score'
            response = requests.get(url=url, headers=headers)
            print("response status when get_comments ", response)
            html_data = response.text

            selector = parsel.Selector(
                html_data)  # 转换数据类型 -->xpath 过时：lxml bs4
            comments_list = selector.xpath(
                '//span[@class="short"]/text()').getall()  # getall()取数据

            with open('./' + work_name + '_短评.txt',
                      mode='a+',
                      encoding='utf-8') as f:

                for comment in comments_list:
                    # print(comment)
                    f.write(comment.replace('\n', ''))
                    f.write('\n')
                    f.write('\n')
        return comments_list
    else:
        with open('./' + work_name + '_短评.txt', mode='a+',
                  encoding='utf-8') as f:
            f.write('NOT FOUND')
        return ['not found']


"""制作词云图"""
def make_wordcloud_pic(comments_list):

    with open('./' + work_name + '_短评.txt', mode='r', encoding='utf-8') as f:
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

    # 词云图的轮廓 
    img = imageio.imread('./outline.png')
    """
    如果不扣图的话就不会识别轮廓，整张图片都是词云
    如果扣的话，词语就会按扣除的轮廓排布
    """

    wc = wordcloud.WordCloud(
        # 长宽可以自己想办法从图片提取吗
        # width=400,
        # height=200,
        background_color='black',
        font_path='msyh.ttc',  # 微软雅黑（系统自带
        mask=img,  # 词云图所用的图片
        scale=10,  # 字体大小 
        stopwords=set([
            line.strip() for line in open(
                './cn_stopwords.txt', mode='r', encoding='utf-8').readlines()
        ]) | current_stopwords  # 停用词即没用的（虚词等）
    )

    # 给词云图输入文字
    wc.generate(txt_list_to_string)

    # 添加赛博朋克风格
    plt.style.use("cyberpunk")
    mplcyberpunk.add_glow_effects()

    # 保存云图
    wc.to_file('./' + work_name + '_短评_词云.png')
    return 0


def make_douban_comments_wordcloud_pic(name):
    global work_name
    work_name = str(name)
    work_href = get_work_href_included_id(work_name)
    work_comments_list = get_comments_list(work_href)
    make_wordcloud_pic(work_comments_list)
    return 0
