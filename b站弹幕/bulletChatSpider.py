# 弹幕爬虫新接口
import os
import re
import csv
import requests


class BulletChatSpiderNew(object):
    '''B站弹幕爬虫'''
    api = "https://api.bilibili.com/x/v2/dm/web/seg.so"
    headers = {
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    }

    def __init__(self, bvid, name):
        self.bvid = bvid
        self.oid = None
        self.pid = None
        self.datas = None
        self.SAVE_TO_PATH = "./bilibili/弹幕文件/"  # 保存文件夹路径
        self.name = name

    def getOidAndPid(self) -> tuple:
        '''获得OID和PID'''
        _url = f"https://www.bilibili.com/video/{self.bvid}"
        _response = requests.get(_url, headers=self.headers)
        pat = re.compile('''"cids":{"1":(.*?)}},"%s":{"aid":(.*?),''' %
                         self.bvid)
        return re.findall(pat, _response.text)[0]

    def bulletChat(self) -> list:
        '''发起弹幕请求'''
        params = {
            "type": 1,
            "oid": self.oid,
            "pid": self.pid,
            "segment_index": 1
        }
        response = requests.get(self.api, headers=self.headers, params=params)
        # with open("li.txt", 'w', encoding="gbk") as f:
        #     f.write(response.text)
        # 正则匹配
        pat = re.compile(".*?([\u4E00-\u9FA5]+).*?")
        return re.findall(pat, response.text)

    def save(self) -> None:
        '''存储'''
        count = 1
        with open(os.path.join(self.SAVE_TO_PATH, f"%s.csv" % self.name),
                  "w",
                  newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(('序号', '内容'))
            for line in self.datas:
                writer.writerow((count, line))
                count += 1
        return

    def loop(self) -> None:
        '''运行'''
        self.oid, self.pid = self.getOidAndPid()
        self.datas = self.bulletChat()
        self.save()
        return


class BulletChatSpiderOld(BulletChatSpiderNew):
    api = "https://comment.bilibili.com/%s.xml"

    def __init__(self, bvid):
        super(BulletChatSpiderOld, self).__init__(bvid, name)

    def bulletChat(self) -> map:
        '''方法重构'''
        self.api = self.api % self.oid
        response = requests.get(self.api, headers=self.headers)
        response.encoding = "utf-8"
        domobj = minidom.parseString(response.text)
        # element_i = domobj.getElementsByTagName('i')[0]
        # 获得根节点
        root = domobj.documentElement
        # 获得子节点 d
        elements_d = root.getElementsByTagName("d")
        # 获得内容
        # print(elements_d[0].getAttribute("p")) # p属性
        return map(lambda d: d.firstChild.nodeValue, elements_d)