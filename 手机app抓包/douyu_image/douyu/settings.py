# -*- coding: utf-8 -*-

BOT_NAME = 'douyu'

SPIDER_MODULES = ['douyu.spiders']
NEWSPIDER_MODULE = 'douyu.spiders'

ROBOTSTXT_OBEY = True

#CONCURRENT_REQUESTS=32
#DOWNLOAD_DELAY=3
#COOKIES_ENABLED=False

DEFAULT_REQUEST_HEADERS = {
    "User-Agent" : "DYZB/1 CFNetwork/808.2.16 Darwin/16.3.0"
    #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
}

ITEM_PIPELINES = {
    'douyu.pipelines.ImagesPipeline': 300,
}

# 图片文件保存路径 
IMAGES_STORE = "C:\Users\Administrator\Desktop\spider\手机app抓包\douyu_image"
