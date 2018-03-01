# -*- coding:utf-8 -*-


from selenium import webdriver
from selenium.webdriver import ActionChains 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from PIL import Image
import time
import os
import functools
import requests
import random
#dcap = dict(DesiredCapabilities.PHANTOMJS)
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36")
#driver = webdriver.PhantomJS(desired_capabilities=dcap)
#driver.get("http://wsjs.saic.gov.cn/txnS02.do?locale=zh_CN&y7bRbP=KGD_qSg8ofg8ofg8idCxIdgrFonJMU.UUxGC23l2Yfg")

#chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
#os.environ['webdriver.chrome.driver'] = chromedriver
#driver = webdriver.Chrome()
url = 'http://wsjs.saic.gov.cn/'

# 重试
def retry(times=3):
    def wrapfunc(func):
        @functools.wraps(func)
        def wrapps(*args,**kwargs):
            i = 0
            res = True
            while i < times:
                try:
                    res = True
                    func(*args,**kwargs)
                    break
                except TimeoutException as e:
                    print(e)
                    res = False
                    print('wait elements timeout retry %d times' % i)
                    i += 1
            return res
        return wrapps
    return wrapfunc

class Spider():
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()
    
    @retry(times=3)
    def get_main_page(self):
        self.driver.get(self.url)
        """cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']
        self.driver.add_cookie(cookies)"""
        #self.driver.set_window_size(1920,1080)

        WebDriverWait(self.driver,5,1).until(
            EC.presence_of_element_located((By.ID,'txnS02'))
            )

    @retry(times=3)
    def get_search_page(self):
        # getElementsByTagName的element加s，定位时，当获取一组标签，element是复数
        self.driver.execute_script('document.getElementById("txnS02").getElementsByTagName("a")[0].click();')
        WebDriverWait(self.driver,5,1).until(
            EC.presence_of_element_located((By.ID,'submitForm'))
            )

    @retry(times=3)
    def get_brand_page(self):
        #self.driver.current_window_handle
        WebDriverWait(self.driver,5,1).until(
            EC.presence_of_element_located((By.NAME,'request:mn'))
            )

        # 模拟人不直接点击
        f = self.driver.find_element_by_tag_name('table')
        ActionChains(self.driver).move_to_element(f).click(f).perform()

        mn = self.driver.find_element_by_name('request:mn')
        ActionChains(self.driver).move_to_element(mn).click(mn).perform()

        self.driver.execute_script('document.getElementsByName("request:mn")[0].value="小米";')
        WebDriverWait(self.driver,5,1).until(
            EC.presence_of_element_located((By.ID,'_searchButton'))
            )
        #submit = self.driver.find_element_by_id('_searchButton')
        #ActionChains(self.driver).move_to_element(submit).click(submit).perform()
        #submit.click()
        self.driver.execute_script('getElementById("_searchButton")[0].click();')
if __name__ == '__main__':

    s = Spider(url)

    s.get_main_page()
    #brand = input('请输入要查询的商标')
    #s.get_s_page(brand)
    s.get_search_page()
    s.get_brand_page()
