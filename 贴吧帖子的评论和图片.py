# coding = utf8


import re
import os
import time
import random
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup

# 清洗数据类
class Tool():
	remove_img = re.compile("")