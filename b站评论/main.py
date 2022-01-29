import json
import re
from urllib.parse import urlencode
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree


# 这个版本保存数据包括回复的评论的信息
class comment_spyder():
    def __init__(self, source_url, video_name):
        self.source_url = source_url  # 传入视频地址
        self.video_name = video_name  # 视频名称
        self.headers = headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'referer': 'https://www.bilibili.com/',
        }
        self.main_root_url = "https://api.bilibili.com/x/v2/reply/main?"  # 评论页api的url
        self.reply_root_url = "https://api.bilibili.com/x/v2/reply/reply?"  # 回复页api的url
        # 评论页url的请求参数
        # next表示评论页数
        # pn表示针对某一条评论的回复的页数
        self.main_query_string_parameters = {
            'jsonp': 'jsonp',
            'next': '1',
            'type': '1',
            'oid': '0',
            'mode': '3',
            'plat': '1',
        }
        # 回复页url的请求参数
        self.reply_query_string_parameters = {
            'jsonp': 'jsonp',
            'pn': '2',
            'type': '1',
            'oid': '0',
            'root': '0'
        }
        # 保存评论
        self.comments_all = {}
        self.comments_main = {}
        self.comments_num = 1

    def parse_source_page(self):
        """从视频地址中解析请求参数"""
        response = requests.get(self.source_url, headers=self.headers)
        text = response.text
        oid = ''.join(
            re.findall(
                r'\d+',
                re.search('<script>window.__INITIAL_STATE__={"aid":\d{1,9}',
                          text).group()))
        self.main_query_string_parameters['oid'] = str(oid)
        self.reply_query_string_parameters['oid'] = str(oid)

    def scratch_comments_and_reply(self, main_json):
        self.comments_main = {}
        """抓取评论回复信息"""
        for i in range(len(main_json["data"]["replies"])):
            # pid
            main_rpid = str(main_json["data"]["replies"][i]['rpid'])
            # 名字
            main_username = main_json["data"]["replies"][i]['member']['uname']
            # 性别
            main_usersex = main_json["data"]["replies"][i]['member']['sex']
            # 等级
            main_userlevel = main_json["data"]["replies"][i]['member'][
                'level_info']["current_level"]
            # 回复数量
            try:
                main_control = main_json["data"]["replies"][i][
                    "reply_control"]["sub_reply_entry_text"]
                main_r_number = int("".join(re.findall(r'\d+', main_control)))
            except:
                main_r_number = 0
            # 点赞数量
            main_comment_like = int(main_json["data"]["replies"][i]['like'])
            # 评论文本
            main_comment = main_json["data"]["replies"][i]["content"][
                "message"]

            # 存储主评论的相关信息
            dict_main = {}
            dict_main['username'] = main_username
            dict_main['sex'] = main_usersex
            dict_main['level'] = main_userlevel
            dict_main['comment'] = main_comment
            dict_main['replies_num'] = main_r_number
            dict_main['like'] = main_comment_like

            dict_main_and_reply = {}
            dict_main_and_reply['main'] = dict_main
            # print("dict_main_and_reply['main'] is ", dict_main_and_reply['main'])

            # reply_comments = []
            # if main_r_number > 0:
            #     self.reply_query_string_parameters['root'] = main_rpid
            #     for j in range(1, (main_r_number - 1) // 20 + 2):
            #         self.reply_query_string_parameters['pn'] = j
            #         reply_page_url = self.reply_root_url + urlencode(
            #             self.reply_query_string_parameters)
            #         reply_page_json = json.loads(
            #             requests.get(reply_page_url).text)
            #         for k in range(len(reply_page_json['data']['replies'])):
            #             reply_username = reply_page_json['data']['replies'][k][
            #                 'member']['uname']
            #             reply_usersex = reply_page_json['data']['replies'][k][
            #                 'member']['sex']
            #             reply_userlevel = reply_page_json['data']['replies'][
            #                 k]['member']['level_info']['current_level']
            #             reply_control = reply_page_json['data']['replies'][k][
            #                 "reply_control"]["sub_reply_entry_text"]
            #             reply_r_number = int("".join(
            #                 re.findall(r'\d+', reply_control)))
            #             reply_comment = reply_page_json['data']['replies'][k][
            #                 'content']['message']
            #             reply_comment_like = reply_page_json['data'][
            #                 'replies'][k]['like']
            #             dict_reply = {
            #                 'username': reply_username,
            #                 'sex': reply_usersex,
            #                 'level': reply_userlevel,
            #                 'comment': reply_comment,
            #                 'replies_num': reply_r_number,
            #                 'like': reply_comment_like,
            #             }
            #             reply_comments.append(dict_reply)
            # dict_main_and_reply['reply'] = reply_comments
            # self.comments_all[str(self.comments_num)] = dict_main_and_reply

            self.comments_main[str(self.comments_num)] = dict_main
            self.comments_num += 1

    def run(self):
        self.parse_source_page()
        main_pn = 1
        main_flag = True
        num = 0
        with open('./bilibili/Comments/%s_评论.json' % self.video_name,
                  'a+',
                  encoding="utf-8") as f:
            f.write('{')
        while main_flag:
            self.main_query_string_parameters['next'] = str(main_pn)
            main_url = self.main_root_url + urlencode(
                self.main_query_string_parameters)
            main_json = json.loads(
                requests.get(main_url, headers=self.headers).text)
            if main_json["data"]["replies"] != None:
                self.scratch_comments_and_reply(main_json)
                print("Page:{},exist {} comments".format(
                    main_pn, len(main_json["data"]["replies"])))
                # 对于评论数很多的视频，最好每次写入一页，但需修改dict格式，使其变成str格式
                l = str(self.comments_main).rstrip('}').lstrip("{") + "},"
                l.replace("'", '"')
                print(l)
                with open('./bilibili/Comments/%s_评论.json' % self.video_name,
                          'a+',
                          encoding="utf-8") as f:
                    # json.dump(self.comments_main, f, ensure_ascii=False)
                    f.write(l)
                main_pn += 1
                time.sleep(2)

            else:
                main_flag = False

        with open('./bilibili/Comments/%s_评论.json' % self.video_name,
                  'a+',
                  encoding="utf-8") as f:
            f.write('}')
        # with open('./bilibili/Comments/comments_all.json', 'w') as f:
        #     json.dump(self.comments_all, f, ensure_ascii=False)
        #     print("Finish writiing the file of comments_all.json")


# 仅仅需要输入视频的url就可以爬取这个视频的评论咯
video_url = 'https://www.bilibili.com/video/BV1QL4y1J74X'
video_name = '【飘飘】《雄狮少年》被骂崇洋媚外，我实在忍不了！'
spyder = comment_spyder(video_url, video_name)
spyder.run()
