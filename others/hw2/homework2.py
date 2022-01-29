from selenium import webdriver
import sys
# 导入 Python 自带的 csv 模块库
import csv
import time

# 要使用chrome driver需要先安装driver
driver = webdriver.Chrome(executable_path='D:\webDriver\chromedriver.exe')
driver.get('https://movie.douban.com/review/best/')
time.sleep(2)

# 获得作者
authorList = []
authors = driver.find_elements_by_class_name('main-hd')
for author in authors:
    author_split = author.text.split()
    authorList.append(author_split[0])

# 展开按钮
buttons = driver.find_elements_by_css_selector('div.main.review-item a.unfold')
for button in buttons:
    time.sleep(2)
    button.click()

time.sleep(2)
short_review = driver.find_elements_by_css_selector('div.short-content')

# 完整影评
full_review = driver.find_elements_by_css_selector('#link-report')
reviewList = []
for review in full_review:
    reviewList.append(review.text)

titles = driver.find_elements_by_css_selector("div.main.review-item > a > img")
titleList = []
for title in titles:
    titleName = title.get_attribute('title')
    titleList.append(titleName)

urlelements = driver.find_elements_by_css_selector("div.main-bd > h2 > a")
urlList = []
for element in urlelements:
    urldata = (element.get_attribute('href'))
    urlList.append(urldata)

# 写入文件
output_csv_file = open('../data/hw2result.csv',
                       'w',
                       newline='',
                       encoding='utf-8')
# 获取输出文件的写指针对象
csv_writer = csv.writer(output_csv_file)
# 输出 csv 文件的表头信息
csv_writer.writerow(['作者', '电影名', 'url', '完整影评'])

for item in zip(authorList, titleList, urlList, reviewList):
    csv_writer.writerow(item)

print('end...')
driver.close