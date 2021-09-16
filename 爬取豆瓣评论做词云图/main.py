import tkinter as tk
# url地址解析
from urllib import parse
# 消息盒子
import tkinter.messagebox as msgbox
# 控制浏览器
import webbrowser
from spider_douban_comments import make_douban_comments_wordcloud_pic as make_pic
from spider_douban_comments import input_stopwords
import re

class App(tk.Tk):
    # 重写构造函数 创建类属性
    def __init__(self):
        super().__init__()

        self.geometry("400x200")
        self.configure(bg='lightGrey')

        # 软件名称
        self.title('豆瓣评论词云生成器')

        # tk对象
        self.work_name = tk.StringVar()
        self.stopwords = tk.StringVar()

        # 控制单选框默认选中的属性
        self.choose = tk.IntVar()
        self.choose.set(1)

        # 软件空间划分
        self.frame_1 = tk.Frame(self)
        self.frame_2 = tk.Frame(self)
        self.frame_3 = tk.Frame(self)
        self.frame_4 = tk.Frame(self)

        # 软件控件内容设置
        self.group = tk.Label(self.frame_1, text='评论来源：', padx=10, pady=10)
        self.tb = tk.Radiobutton(self.frame_1,
                            text='豆瓣',
                            variable=self.choose,
                            value=1,
                            width=10,
                            height=3)

        self.for_prompht_workname = tk.Label(self.frame_2, text='enter a book | movie | music：',bg = 'Cornsilk', fg='PaleGreen')
        self.for_work_name = tk.Entry(self.frame_2,
                         textvariable=self.work_name,
                         highlightcolor='Fuchsia',
                         highlightthickness=1,
                         width=30)

        self.for_prompht_stopwords  = tk.Label(self.frame_3, text='enter some stopwords：', bg = 'Cornsilk',fg='lightGrey')
        self.for_stopwords = tk.Entry(self.frame_3,
                         textvariable=self.stopwords,
                         highlightcolor='Fuchsia',
                         highlightthickness=1,
                         width=30)   

        self.for_make = tk.Button(self.frame_4,
                         text='生成',
                         font=('楷体', 12),
                         fg='Purple',
                         width=2,
                         height=1,
                         command=self.make)

        # 控件布局
        '''
        激活空间，即固定位置
        '''
        self.frame_1.pack()
        self.frame_2.pack()
        self.frame_3.pack()
        self.frame_4.pack()

        '''
        位置确定
        '''
        # grid 宫格
        self.group.grid(row=0, column=0)
        self.tb.grid(row=0, column=1)

        '''
        空间2的控件位置无需看空间1的位置
        空间与空间之间是独立的
        '''
        ############## frame 2 ###############
        self.for_prompht_workname.grid(row=0, column=0)
        self.for_work_name.grid(row=0, column=1)
        ############## frame 3 ###############
        self.for_prompht_stopwords.grid(row=0, column=0)
        self.for_stopwords.grid(row=0, column=1)
        ############## frame 4 ###############
        self.for_make.grid(row=0, column=2, ipadx=20, ipady=10)

    # 定义播放按钮的事件函数
    '''
    解析电影
    '''
    def make(self):
        stopwords = set( self.stopwords.get().split(" "))
        # print("stopwords is ", stopwords)
        input_stopwords(stopwords)
        make_pic(self.work_name.get())

    # 启动
    def loop(self):
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.loop()
