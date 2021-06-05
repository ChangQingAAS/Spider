import re
import requests
from selenium import webdriver
import csv
import time


def get_product(keyboard):
    """搜索商品"""
    # 最大化浏览器
    driver.maximize_window()
    # 找到输入框，输入关键字
    driver.find_element_by_css_selector('#key').send_keys(keyboard)
    driver.find_element_by_css_selector(
        '#search > div > div.form > button').click()
    # 隐式等待,等待渲染和加载数据，如果提前加载完就不等这么长时间了
    driver.implicitly_wait(10)


# 数据的懒加载（浏览器向下拉动页面，下面的数据才会显示）
def drop_down():
    """模拟任务滚动鼠标向下拉动页面"""
    for x in range(1, 11, 2):
        time.sleep(0.5)
        j = x / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)


def parse_data():
    """解析商品数据"""
    lis = driver.find_elements_by_css_selector('.gl-item')
    for li in lis:
        try:
            name = li.find_element_by_css_selector('div .p-name a em').text
            price = li.find_element_by_css_selector(
                'div .p-price strong i').text
            deal = li.find_element_by_css_selector(
                'div .p-commit strong a').text  # 评论
            shop = li.find_element_by_css_selector(
                'span.J_im_icon a').text  # 店铺名
            # print(name, price, deal, shop)
            with open('spider/京东商品' + word + '数据.csv',
                      mode='a+',
                      encoding='utf-8',
                      newline='\n') as f:
                csv_write = csv.writer(f)  # 一个写入csv文件类型的对象
                csv_write.writerow([name, shop, deal, price])
        except Exception as e:
            print(e)


def get_next():
    """找到下一页，点击"""
    driver.find_element_by_css_selector(
        '#J_bottomPage > span.p-num > a.pn-next > em').click()


word = input('请输入你想搜索的商品：')
# 实例化浏览器驱动
driver = webdriver.Edge(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
driver.get('https://www.jd.com/')

# 调用搜索商品的函数
get_product(word)
with open('spider/京东商品' + word + '数据.csv',
          mode='a+',
          encoding='utf-8',
          newline='\n') as f:
    csv_write = csv.writer(f)  # 一个写入csv文件类型的对象
    csv_write.writerow(['商品名称', '店铺', '评论数', '价格'])
for page in range(1, 10):
    # 下拉页面的函数
    drop_down()
    # 解析数据的函数
    parse_data()
    # 进入下一页
    get_next()

# 退出浏览器
driver.quit()
