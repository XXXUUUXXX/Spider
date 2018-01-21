# -*- coding: utf-8 -*-


BOT_NAME = 'toutiao'

SPIDER_MODULES = ['toutiao.spiders']
NEWSPIDER_MODULE = 'toutiao.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 2

COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
   'Connection': 'keep-alive',
   'Accept-Encoding': 'gzip',
   'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
}

ITEM_PIPELINES = {
    'toutiao.pipelines.ToutiaoPipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'toutiao'
MONGODB_SHEETNAME = 'comment'
