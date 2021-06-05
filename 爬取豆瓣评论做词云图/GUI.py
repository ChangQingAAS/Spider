import re
import tkinter as tk
# url地址解析
from urllib import parse
# 消息盒子
import tkinter.messagebox as msgbox
# 控制浏览器
import webbrowser
import pa_豆瓣


class App():
    # 重写构造函数 创建类属性
    def __init__(self, width=800, height=600):
        # 创建自定义类属性
        self.w = width
        self.h = height

        # 软件名称
        self.title = '评论词云生成器'
        # tk对象
        self.root = tk.Tk(className=self.title)
        self.work_name = tk.StringVar()
        # 控制单选框默认选中的属性
        self.v = tk.IntVar()
        self.v.set(1)

        # 软件空间划分
        frame_1 = tk.Frame(self.root)
        frame_2 = tk.Frame(self.root)

        # 软件控件内容设置
        group = tk.Label(frame_1, text='评论来源：', padx=10, pady=10)
        tb = tk.Radiobutton(frame_1,
                            text='豆瓣',
                            variable=self.v,
                            value=1,
                            width=10,
                            height=3)
        label = tk.Label(frame_2, text='请输入你想查看的书籍或影视或音乐：')
        entry = tk.Entry(frame_2,
                         textvariable=self.work_name,
                         highlightcolor='Fuchsia',
                         highlightthickness=1,
                         width=30)
        play = tk.Button(frame_2,
                         text='生成',
                         font=('楷体', 12),
                         fg='Purple',
                         width=2,
                         height=1,
                         command=self.make)

        # 控件布局
        '''
        激活空间
        '''
        frame_1.pack()
        frame_2.pack()
        '''
        位置确定
        '''
        # grid 宫格
        group.grid(row=0, column=0)
        tb.grid(row=0, column=1)
        '''
        空间2的控件位置无需看空间1的位置
        空间与空间之间是独立的
        '''
        label.grid(row=0, column=0)
        entry.grid(row=0, column=1)
        play.grid(row=0, column=2, ipadx=20, ipady=10)

    # 定义播放按钮的事件函数
    '''
    解析电影
    '''

    def make(self):
        # print('self.work_name in GUI.py is ', self.work_name.get())
        pa_豆瓣.main(self.work_name.get())

    # 如何启动
    def loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.loop()
