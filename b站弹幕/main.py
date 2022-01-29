# B站弹幕爬虫
from bilibliApp import BilibiliApp

if __name__ == "__main__":
    BVID = "BV1gS4y1M7x3"
    name = "【雄狮少年】热度过去，我终于敢讲了，电影就是有问题！" + '_视频弹幕'
    BilibiliApp(BVID, name, mode=True).bulletChat()
