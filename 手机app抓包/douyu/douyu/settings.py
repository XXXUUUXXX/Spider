# -*- coding: utf-8 -*-


BOT_NAME = 'douyu'

SPIDER_MODULES = ['douyu.spiders']
NEWSPIDER_MODULE = 'douyu.spiders'

ROBOTSTXT_OBEY = True

#CONCURRENT_REQUESTS = 1
#DOWNLOAD_DELAY = 5

COOKIES_ENABLED = False

#DEFAULT_REQUEST_HEADERS = {
#   'Connection': 'Keep-Alive',
#   'Accept-Encoding': 'gzip',
#   'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
#}

ITEM_PIPELINES = {
    'douyu.pipelines.DouyuPipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'douyu'
MONGODB_SHEETNAME = 'juediqiusheng'

# 解决HTTP status code is not handled or not allowed问题以及DEBUG: Crawled (403)
HTTPERROR_ALLOWED_CODES = [403]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
    'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
]

DOWNLOADER_MIDDLEWARES = {
    'douyu.middlewares.RandomUserAgent': 100,
    'douyu.middlewares.RandomProxy': 200,
}

