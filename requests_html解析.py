# -*- coding:utf-8 -*-

from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://www.python.org/')
# 抓取页面上所有链接的列表
link = r.html.links  
#print(link)
# 以绝对形式抓取页面上所有链接的列表(锚点除外)
r.html.absolute_links 
# 使用CSS选择器选择一个元素
about = r.html.find('#about',first = True)
#print(about.text)     # The text content of theclass:`Element <Element>` or :class:`HTML <HTML>
#print(about.attrs)    # Returns a dictionary of the attributes of the :class:`Element <Element>
#print(about.html)     # 返回html元素
#print(about.find('a')) # 选择元素内部的元素
#print(about.absolute_links) #搜索元素内的绝对链接
# 搜索页面上的文字
text = r.html.search('Python is a {} language')[0]
#print(text)
# 使用xpath选择元素
text1 = r.html.xpath('//li[@id="downloads"]/a')
#print(text1)

"""JavaScript"""
# 抓取由JavaScript产生的文本
j = session.get('http://python-requests.org')
# render(self, retries: int = 8, script: str = None, scrolldown=False, sleep: int = 0, reload: bool = True)方法
# 在Chromium中重新加载响应，并用JavaScript更新版本替换HTML内容，同时执行JavaScript。
# retries     Chromium中重新加载页面的次数。
# script      要在页面加载时执行的JavaScript（可选）
# scrolldown  整数（如果提供）多少次下翻
# sleep       整数（如果提供）在初始渲染后多长时间睡眠
# reload      如果“False”，内容将不会从浏览器加载，而是从内存中提供。
j = j.html.render()
month = j.html.search('Python 2 will retire in only {months} months!')['months']
print(month)

"""无session"""
from requests_html import HTML
doc = """<a href='https://httpbin.org'>"""
html = HTML(html=doc)
link = html.links
#print(link)