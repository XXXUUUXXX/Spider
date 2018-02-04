# -*- coding:utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://cuijiahua.com/blog/2018/01/spider_4.html')
b = BeautifulSoup(html.read())
print(b.h1)