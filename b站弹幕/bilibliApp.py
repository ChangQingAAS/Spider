from bulletChatSpider import BulletChatSpiderNew, BulletChatSpiderOld


class BilibiliApp(object):
    def __init__(self, bvid, name, mode=False):
        '''
        :param bvid: 视频BVID
        :param mode: 使用爬取弹幕接口，默认`旧接口`
        '''
        self.bvid = bvid
        self.mode = mode
        self.name = name

    def bulletChat(self) -> None:
        if self.mode == True:
            '''使用新接口'''
            BulletChatSpiderNew(self.bvid, self.name).loop()
        else:
            '''使用旧接口'''
            BulletChatSpiderOld(self.bvid, self.name).loop()
        return

    def run(self) -> None:
        '''运行'''
        self.bulletChat()
