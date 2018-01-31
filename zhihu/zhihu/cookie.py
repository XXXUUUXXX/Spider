# -*- coding:utf-8 -*-

#修改spider_name为spiderName
import os
import time
import json
import logging
from .yundama import identify
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


METHOD = 0 # 0手动输入验证码， 1云打码， 2机器识别 

myZhiHu = [('account', 'password', 0),] # 0手机， 1邮箱

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
    #code_text = captcha(captcha_data)
"""

def get_cookie(account, password, way):
    if way == 0:
        login_URL = 'https://www.zhihua.com/login/phone_num'
        username = 'phone_num'
    else:
        login_URL = 'https://www.zhihu.com/login/email'
        username = 'email'
    try:
        # 调用环境变量指定的PhantomJS浏览器创建浏览器对象
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
                    code_text = input('请输入验证码：') 
                #elif METHOD == 2:
                    #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
                    #captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)
                    # 发送图片的请求，获取图片数据流
                    #captcha_data = requests.Session.get(captcha_url, headers = headers).content
                    #code_text = captcha(captcha_data)
                else:
                    img = login_DIV.find_element_by_class_name('captcha')
                    x = img.location['x']
                    y = img.location['y']
                    image = Image.open('zhihu.png')
                    image.crop((x, y, 85+x, y+30)).save('captcha.png')
                    code_text = identify()
                login_DIV.find_element_by_name('captcha').send_keys(code_text)
            # 点击登录按钮
            login_DIV.find_element_by_class_name('zg-btn-blue').click()
            time.sleep(3)
            # 验证码或账号密码错误时退出循环
            try:
                login_DIV.find_element_by_class_name('error')
                logger.warning('验证码或账号密码错误%s'% account)
            except:
                break
        try:
            # 登录成功，右上角显示用户
            driver.find_element_by_class_name('top-nav-profile')
            cookie = {}
            # 获取页面每个cookie值
            for elem in driver.get_cookies():
                cookie[elem['name']] = elem['value']
            logger.warning('Get Cookie Success-(Account:%s)' % account)
            # 返回json格式的cookie(str)
            return json.dumps(cookie)
        except Exception:
            logger.warning('Failed -%s' % account)
            return ''
    # 对应第一个try        
    except Exception:
        logger.warning('Failed -%s' % account)
        return ''
    finally:
        try:
            # 关闭浏览器
            driver.quit()
        except Exception:
            pass

def update_cookie(account, cookie):
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_window_size(1920, 1080)
    driver.get('https://www.zhihu.com')
    # 删除所有Cookies
    driver.delete_all_cookies()
    send_cookie = []
    for key, value in cookie.items():
        one = {}
        one = {'domain': '.zhihu.com', 'name': key, 'value': value, 'path': '/', 'expiry': None}
        # 添加Cookie
        driver.add_cookie({k: one[k] for k in ('name', 'value', 'domain', 'path', 'expiry')})
    # 系统检测到您的帐号或IP存在异常流量，请输入以下字符用于确认这些请求不是自动程序发出的
    driver.get('https://www.zhihu.com/account/unhuman?type=unhuman&message=%E7%B3%BB%E7%BB%9F%E6%A3%80%E6%B5%8B%E5%88%B0%E6%82%A8%E7%9A%84%E5%B8%90%E5%8F%B7%E6%88%96IP%E5%AD%98%E5%9C%A8%E5%BC%82%E5%B8%B8%E6%B5%81%E9%87%8F%EF%BC%8C%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BB%A5%E4%B8%8B%E5%AD%97%E7%AC%A6%E7%94%A8%E4%BA%8E%E7%A1%AE%E8%AE%A4%E8%BF%99%E4%BA%9B%E8%AF%B7%E6%B1%82%E4%B8%8D%E6%98%AF%E8%87%AA%E5%8A%A8%E7%A8%8B%E5%BA%8F%E5%8F%91%E5%87%BA%E7%9A%84')
    time.sleep(1)
    driver.save_screenshot('update.png')
    if METHOD == 0:
        code_text = input('请输入验证码：')
    #elif METHOD == 2:
        #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
        #captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login" % (time.time() * 1000)
        # 发送图片的请求，获取图片数据流
        #captcha_data = requests.Session.get(captcha_url, headers = headers).content
        #code_text = captcha(captcha_data)
    else:
        img = login_DIV.find_element_by_class_name('Unhuman-captcha')
        x = img.location['x']
        y = img.location['y']
        image = Image.open('zhihu.png')
        image.crop((x, y, 85+x, y+30)).save('captcha.png')
        code_text = identify()
    driver.find_element_by_class_name('Input').send_keys(code_text)
    driver.find_element_by_class_name('Button--blue').click()
    time.sleep(3)
    try:
        driver.find_element_by_class_name('AppHeader-profile')
        cookie = {}
        for elem in driver.get_cookies():
            cookie[elem['name']] = elem['value']
        logger.warning('Update Cookie Success-(Account:%s)' % account)
        return json.dumps(cookie)
    except Exception:
        logger.warning('Update Failed-%s' % account)
        return ''
    finally:
        try:
            driver.quit()
        except Exception:
            pass

def init_cookie(rconn, spiderName):
    """获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。"""
    for zhihu in myZhiHu:
        if rconn.get('%s:Cookies:%s--%s' % (spiderName, zhihu[0], zhihu[1])) is None:
            # 调用get_cookie函数获取cookie
            cookie = get_cookie(zhihu[0],zhihu[1],zhihu[2])
            if len(cookie) > 0:
                rconn.set('%s:Cookies:%s--%s' % (spiderName, zhihu[0], zhihu[1]), cookie)
    cookie_num = str(rconn.keys()).count('zhihuspider:Cookies')
    logger.warning('The num of the cookies is %s' % cookie_num)
    if cookie_num == 0:
        logger.warning('stopping.....')
        os.system('pause')

def update_one_cookie(account_text, rconn, spiderName, cookie):
    """ 更新一个账号的Cookie """
    account = account_text.split('--')[0]
    # 调用update_cookie函数更新cookie
    new_cookie = update_cookie(account, cookie)
    if len(new_cookie) > 0:
        logger.warning('The cookie of %s has been updated successfully!' % account)
        rconn.set('%s:Cookies:%s' % (spiderName, account_text), new_cookie)
    else:
        logger.warning('The cookie of %s updated failed! Remove it' % account_text)
        remove_cookie(account_text, rconn, spiderName)

def remove_cookie(account_text, rconn, spiderName):
    """ 删除某个账号的Cookie """
    rconn.delete('%s:Cookies:%s' % (spiderName, account_text))
    cookie_num = str(rconn.keys()).count('zhihuspider:Cookies')
    logger.warning('The num of the cookies left is %s' % cookie_num)
    if cookie_num == 0:
        logger.warning('stopping....')
        os.system('pause')

if __name__ == '__main__':
    get_cookie(myZhiHu[0][0], myZhiHu[0][1], myZhiHu[0][2])