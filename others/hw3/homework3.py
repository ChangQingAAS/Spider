from requests.exceptions import RequestException
import re
import time
import requests
import json
import pandas as pd
import numpy as np


def prepare_data(movie_id, movie_name):
    print("===================获取影评数据======================")
    # 模拟浏览器，需要提供header头部信息
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
    }
    comment_pd = pd.DataFrame()
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    for i in range(0, 10000, 15):
        print("爬取第{0}页".format(int((i + 15) / 15)))
        # i%1000是因为爬猫眼时偏移量最大只能1000
        url = "http://m.maoyan.com/mmdb/comments/movie/" + str(
            movie_id) + ".json?_v_=yes&offset=" + str(
                i % 1000) + "&startTime=" + startTime
        html = requests.get(url, headers=headers)
        time.sleep(3)
        res_data = html.content  # 提取content内容
        res_data = res_data.decode("utf-8")  # 对内容解码

        # json.loads():反序列化成标准的Json格式
        json_data = json.loads(res_data)
        # 提取Json数据
        # 先判断是否有数据
        if "cmts" in json_data:
            # 提取cmts评论
            cmts = json_data["cmts"]
            # 选取数据
            for cmt in cmts:
                # 昵称，性别，评论星级，点赞数，回复数，城市，日期，评论内容
                cmt_dict = {}
                # 昵称
                if "nick" in cmt.keys():
                    cmt_dict["nick"] = cmt["nick"]
                else:
                    cmt_dict["nick"] = np.nan
                # 性别
                if "gender" in cmt.keys():
                    cmt_dict["gender"] = cmt["gender"]
                else:
                    cmt_dict["gender"] = np.nan
                # 评分
                if "score" in cmt.keys():
                    cmt_dict["score"] = cmt["score"]
                else:
                    cmt_dict["score"] = np.nan
                # 点赞数
                if "approve" in cmt.keys():
                    cmt_dict["approve"] = cmt["approve"]
                else:
                    cmt_dict["approve"] = np.nan
                # 评论的回复数量
                if "replyCount" in cmt.keys():
                    cmt_dict["replyCount"] = cmt["replyCount"]
                else:
                    cmt_dict["replyCount"] = np.nan
                # 城市
                if "cityName" in cmt.keys():
                    cmt_dict["cityName"] = cmt["cityName"]
                else:
                    cmt_dict["cityName"] = np.nan
                # 日期
                if "time" in cmt.keys():
                    cmt_dict["time"] = cmt["time"]
                else:
                    cmt_dict["time"] = np.nan
                # 评论内容
                if "content" in cmt.keys():
                    cmt_dict["content"] = cmt["content"]
                else:
                    cmt_dict["content"] = np.nan

                comment_pd = comment_pd.append(cmt_dict, ignore_index=True)
            print(comment_pd)
        else:
            print("No data")

    comment_pd.to_excel(str(movie_name) + ".xlsx")
    print("===================数据获取完毕======================")


movie_id = 1210778
movie_name = "花木兰"

prepare_data(movie_id, movie_name)

#爬取猫眼电影信息


def get_one_page(url):
    #增加了User-Agent识别，需要在headers中添加User-Agent参数。
    try:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


    #正则提取
def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a' +
        '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>' +
        '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    #遍历提取结果并生成字典
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


    #写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


for i in range(10):
    main(offset=i * 10)
    #延时等待
    time.sleep(1)
