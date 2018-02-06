# -*-coding:utf-8 -*-

"""
    Selenium模拟用户滑动解锁
    简单，方便更新
    速度慢，不能制作成api接口的形式
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
class Crack():
    def __init__(self,keyword):
        self.url = 'http://bj.gsxt.gov.cn/sydq/loginSydqAction!sydq.dhtml';
        self.browser = webdriver.Chrome('D:\\chromedriver.exe')
        self.wait = WebDriverWait(self.browser, 100)
        self.keyword = keyword
    def open(self):
        """
        打开浏览器,并输入查询内容
        """
        self.browser.get(self.url)
        keyword = self.wait.until(EC.presence_of_element_located((By.ID, 'keyword_qycx')))
        bowton = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn')))
        keyword.send_keys(self.keyword)
        bowton.click()
    def crack(self):
        # 打开浏览器
        self.open()
if __name__ == '__main__':
    print('开始验证')
    crack = Crack(u'中国移动')
    crack.crack()