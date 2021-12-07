import requests
from selenium import webdriver

not_test_ID_list = [3019225055]

# 清空文件
with open("./physical_test/data.txt", mode="w") as f:
    pass

# 实例化浏览器驱动
driver = webdriver.Edge(
    "C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")
# 最大化浏览器
# driver.maximize_window()

# 本专业的边界我知道，但是我该怎么知道其他专业的边界值呢，怎么进行exception处理呢？
# TODO
for user_id in range(3019225139, 3019225200):

    # 如果每次就退出
    if user_id in not_test_ID_list:
        with open("./physical_test/data.txt", mode="a+") as f:
            f.write(str(user_id) + " don't test! \n")
            f.write("\n")
            f.write("\n")
        continue

    driver.get('http://test.tfht.com.cn/Wap')

    # 找到输入框，输入关键字
    driver.find_element_by_css_selector('#username').send_keys(user_id)
    driver.find_element_by_css_selector('#password').send_keys(user_id)
    driver.find_element_by_css_selector('#frm_login > div.ui-btn-wrap').click()
    driver.implicitly_wait(10)

    try:
        # 如果这个人没测，就会弹出弹窗,然后点一下，但是好像有时候不管用
        al = driver.switch_to_alert()
        al.accept()
        driver.implicitly_wait(10)
    except:
        pass

    try:
        # 隐式等待,等待渲染和加载数据，如果提前加载完就不等这么长时间了
        name = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(1) > div.u_nav_name').text
        student_id = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(2) > div.u_nav_name').text
        year = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(3) > div.u_nav_name').text
        gender = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(4) > div.u_nav_name').text
        birthday = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(5) > div.u_nav_name').text
        birthplace = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(6) > div.u_nav_name').text
        classes = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(7) > div.u_nav_name').text
        scores = driver.find_element_by_css_selector(
            '#mycenter >  li:nth-child(8) > div.u_nav_name').text

        with open("./physical_test/data.txt", mode="a+") as f:
            f.write(name + "\n")
            f.write(student_id + "\n")
            f.write(year + "\n")
            f.write(gender + "\n")
            f.write(birthday + "\n")
            f.write(birthplace + "\n")
            f.write(classes + "\n")
            f.write(scores + "\n")
            f.write("\n")
            f.write("\n")
    except:
        with open("./physical_test/data.txt", mode="a+") as f:
            f.write(str(user_id) + " don't test! \n")
            f.write("\n")
            f.write("\n")