"""
猫眼电影的票房等数据（数字）设置了文字反爬机制
不同于起点中文网能直接看见ttf文件，猫眼的数字反爬更复杂些，主要表现在：
进行了web上的base64编码，并且每次刷新都会变化
通过FontTools可生成ttf和xml文件，但是每次运行生成的文件都不一样
需要找寻其内部固定的映射关系
"""
import requests, time, re, pprint, base64
from fontTools.ttLib import TTFont
from io import BytesIO
from lxml import etree


def get_relation(url):
    """
    获取网页源代码中的font—face中的内容，并保存成.ttf格式的文件
    :param url: <str> 需要解析的网页地址
    :return:<dict> 网页字体（动态变化的）编码与阿拉伯数字的映射关系
    """
    #获取网页源代码中的font—face中的内容
    font_face = re.findall('base64,(.*?)\) format', html_data.text, re.S)[0]
    #print(font_face)
    #保存成.ttf格式的文件
    b = base64.b64decode(font_face)
    with open('font_face.ttf', 'wb') as f:
        f.write(b)
    font = TTFont('font_face.ttf')
    font.saveXML('font_face.xml')  #将ttf文件生成xml文件并保存到本地
    codelist = font.getGlyphNames()[1:-1]  # 第一个和最后一元素不是0-9的编码
    font_local = TTFont('font_face_local.ttf')
    font_local.saveXML('font_face_local.xml')
    codelist_local = font_local.getGlyphNames()[1:-1]  #第一个和最后一元素不是0-9的编码
    print('codelist:', codelist_local)
    fontdict_local = {
        'uniE346': 7,
        'uniE3DB': 2,
        'uniE4AC': 4,
        'uniE6BF': 5,
        'uniEA17': 0,
        'uniEBBC': 1,
        'uniEF7E': 9,
        'uniF227': 3,
        'uniF4C0': 8,
        'uniF551': 6
    }
    key = []
    value = []
    for i in codelist_local:
        obj_local = font_local['glyf'][i]  #获取本地字体文件数字0-9的编码对象
        print('obj_local:', obj_local)
        for k in codelist:
            obj = font['glyf'][k]
            #print('obj:',obj)
            if obj == obj_local:
                #print(k,fontdict_local[i])
                key.append(k.strip('uni'))
                value.append(fontdict_local[i])
    dict_relation = dict(zip(key, value))  #网页字体（动态变化的）编码与阿拉伯数字的映射关系

    #print('网络文字映射关系：')
    #pprint.pprint(dict_relation)
    return dict_relation


def get_decode_font(numberlist, relation):
    """
    对反爬数字进行解码
    :param numberlist: <list> 直接从网页源代码re获得的需要解码的数字
    :param relation: <dict> 解码所需的映射关系
    :return: <str> 解码后的数字
    """
    data = ''
    for i in numberlist:
        numbers = i.replace('&#x', '').upper()
        #print(numbers)
        #小数点没有单独成为里列表的元素，与后面的数字写在了一起，需要判断下
        if len(numbers) == 5:
            data += '.'
            numbers = numbers.strip('.')
            #print('numbers:',numbers)
        fanpa_data = str(relation[numbers])
        data += fanpa_data
    print('实时票房（万元）:', data + '\n')


    #return data
def get_movie_info(url):
    """
    爬取网页的影片名称和实时票房（网页源代码中未解码的数字）
    :param url:
    :return:
    """
    selector = etree.HTML(html_data.text)
    infos = selector.xpath('//*[@id="ticket_tbody"]/ul')
    boxes = re.findall('<b><i class="cs">(.*?)</i>', html_data.text, re.S)
    for info, i in zip(infos, boxes):
        movie_name = info.xpath('li[1]/b/text()')[0]
        movie_box = i.split(';')[0:-1]
        print('影片名称:', movie_name)
        #print('网页直接获取的影片实时票房:',movie_box)#一维列表形式
        relation = get_relation(url)
        get_decode_font(movie_box, relation)


url = 'https://piaofang.maoyan.com/?ver=normal'
headers = {
    'User-Agent':
    'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
html_data = requests.get(url, headers=headers)
get_movie_info(url)