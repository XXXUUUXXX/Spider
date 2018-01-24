# -*- coding:utf-8 -*-

import os
import time
import json
import logging
#from .yundama import identify
# 导入webdriver
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from bs4 import BeautifulSoup
from PIL import Image
from pytesseract import image_to_string

# ---------------------------selenium设置phantomjs请求头-------------------------
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
)
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
#driver.get("https://httpbin.org/get?show_env=1")
#driver.get_screenshot_as_file('01.png')
#driver.quit()
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING) # 将selenium的日志级别设成WARNING
#-------------------------------------------------------------------------------


METHOD = 0 # 0手动输入验证码(tesseract识别)， 1云打码

myZhiHu = [('account', 'password', 0)] # 0手机， 1邮箱

"""
def captcha(captcha_data):
    with open('captcha.jpg', 'wb') as f:
        f.write(captcha_data)
        time.sleep(1)

    image = Image.open('captcha.jpg')
    text = image_to_string(imgae)
    print('机器识别验证码：' + text.encode('utf-8'))
    command = input("输入Y表示验证正确，同意使用(输入其他键自行输入):")
    if (command == "Y" or command == "y"):
        return text
    else:
        return input("请输入验证码：")

def get_captcha():
    # 构建一个Session对象，可以保存页面Cookie
    sess = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)
    # 发送图片的请求，获取图片数据流
    captcha_data = sess.get(captcha_url, headers = headers).content
    code_text = captcha(captcha_data)
"""

def get_cookie(account, password, way):
    if way == 0:
        login_URL = 'https://www.zhihua.com/login/phone_num'
        username = 'phone_num'
    else:
        login_URL = 'https://www.zhihu.com/login/email'
        username = 'email'
    try:
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        # 设置分辨率
        driver.set_window_size(1920,1080)
        # 在此页面进行操作
        driver.get('https://www.zhihu.com/explore')
        time.sleep(1)
        # 点击登录，显示账号和密码框
        driver.find_element_by_class_name('switch-to-login').click()
        # selenium + phantomjs 使用时查看页面中关键字有几个，防止错误，如：class="LoginForm"有两个，应往上一级扩增一级
        login_DIV = driver.find_element_by_id('SidebarSignFlow').find_element_by_class_name('LoginForm')
        # 输入账号
        login_DIV.find_element_by_name('account').send_keys(account)
        # 输入密码
        login_DIV.find_element_by_name('password').send_keys(password)
        time.sleep(1)

        while True:
            # 保存截图
            driver.save_screenshot('zhihu.png')
            # 有验证码
            if login_DIV.find_element_by_class_name('captcha-module').get_attribute('style') != '':
                if METHOD == 0: