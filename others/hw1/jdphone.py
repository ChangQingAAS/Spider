from selenium import webdriver
import time
import pandas as pd
import os

# 声明要爬取的页面url地址
url = 'https://list.jd.com/list.html?cat=9987,653,655&page=1'
# 创建模拟Chrome浏览器对象
browser = webdriver.Chrome(executable_path='D:\webDriver\chromedriver.exe')
# 使用浏览器对象打开指定url的页面
browser.get(url)
# 休眠2秒，保证所有的页面数据下载到本地
time.sleep(2)
# 使用分析得出的类选择器，获取当前页面的所有的手机的名称信息和价格信息的标签
all_product_names = browser.find_elements_by_css_selector(
    '#plist > ul > li > div > div.p-name > a > em')
all_produce_prices = browser.find_elements_by_css_selector(
    '#plist > ul > li > div > div.p-price > strong:nth-child(1) > i')

# 声明用来存放单一手机名称和价格的列表list，其中含有两个列表元素，分别为手机的名称，手机的价格
name_price_list = []
# 声明存放所有的手机的名称和价格的列表list，相当于一个二维列表list，其中每个元素是上面的一个具体的name_price_list
all_name_price_list = []
# 遍历所有手机的名称和价格信息，打印输出同时放入all_name_price_list二维列表中
# 使用zip函数，一次性遍历两个list列表
for name, price in zip(all_product_names, all_produce_prices):
    # 获取手机名称信息标签的标签体文本，即：手机的名称
    product_name_text = name.text
    # 去除名称包含的“京东精选”、“TOPLIFE”等前缀文字信息
    if product_name_text.find('\n') > 0:
        product_name_text = product_name_text[product_name_text.find('\n') +
                                              1:]
    # 获取手机价格信息标签的标签体文本，即：手机的价格
    produce_price_text = price.text
    # 打印每个手机的名称和价格信息
    print(product_name_text, produce_price_text)
    # 将每个手机的名称信息、价格信息放入 name_price_list 列表中
    name_price_list.append(product_name_text)
    name_price_list.append(produce_price_text)
    # 将含有每个手机的名称信息，价格信息元素的 name_price_list 列表加入存放所有的手机的名称和价格的列表 all_name_price_list 中
    all_name_price_list.append(name_price_list)
    # 清空 name_price_list，准备存放下一个手机的名称信息、价格信息
    name_price_list = []

# 打印存放所有的手机的名称和价格的列表 all_name_price_list
print(all_name_price_list)
# 将 all_name_price_list 放入 pandas 的 DataFrame 的变量 test 中
test = pd.DataFrame(data=all_name_price_list)
# 打印 test
print(test)

proDir = os.getcwd()
newDir = os.path.join(proDir, "data")
if not os.path.exists(newDir):
    os.mkdir(newDir)

# 将 test 保存到当前文件夹下的 testcsv.csv 文件中，使用 gbk 编码字符集，csv 文件不含行索引，不含表头元素
test.to_csv('data/testcsv.csv', encoding='gbk', index=False, header=False)

# 关闭浏览器对象
browser.close()
