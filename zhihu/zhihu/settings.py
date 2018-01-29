# -*- coding: utf-8 -*-

BOT_NAME = 'zhihu'
SPIDER_MODULES = ['zhihu.spiders']
NEWSPIDER_MODULE = 'zhihu.spiders'


# 重定向关闭
REDIRECT_ENABLED = False
# 包括第一次下载，最多重试次数
RETRY_TIMES = 1
#下载超时时间
DOWNLOAD_TIMEOUT = 10 


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'


# 使用了scrapy-redis里的去重组件，不使用scrapy默认的去重
DUPEFILTER_CLASS = "zhihu.scrapy_redis.dupefilter.RFPDupeFilter"
# 使用了scrapy-redis里的调度器组件，不使用scrapy默认的调度器
SCHEDULER = "zhihu.scrapy_redis.scheduler.Scheduler"
# 允许暂停，redis请求记录不会丢失
SCHEDULER_PERSIST = True
# 队列形式，请求先进先出
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"


# 种子队列
REDIS_HOST = "127.0.0.1" # 指定数据库的主机IP
REDIS_PORT = 6379 # 指定数据库的端口号
REDIS_URL = None # 多台主机部署分布式爬虫时，在REDIS_URL中填入连接redis的主机URL

# 去重队列
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0
# REDIS_QUEUE_NAME = 'OneName'   # 如果不设置或者设置为None，则使用默认的，每个spider使用不同的去重队列和种子队列。如果设置了，则不同spider共用去重队列和种子队列



# 主机名
MONGODB_HOST = '127.0.0.1'
# 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DNNAME = 'zhihu'
# 存放数据的表名称
#MONGODB_SHEETNAME = ''


DOWNLOADER_MIDDLEWARES = {
    'zhihu.middlewares.RandomUserAgent': 100,
    'zhihu.middlewares.RandomProxy': 200,
    'zhihu.middlewares.CookiesMiddleware': 300,
    
    #'zhihu.middlewares.ZhihuDownloaderMiddleware': 543,
}


ITEM_PIPELINES = {
    'zhihu.pipelines.ZhihuPipeline': 300,
}


'''
DOWNLOAD_DELAY = 3
#启动自动限速扩展
AUTOTHROTTLE_ENABLED = True
# 初始下载延迟（秒）
AUTOTHROTTLE_START_DELAY = 3
# 在高延迟情况下最大的下载延迟
AUTOTHROTTLE_MAX_DELAY = 60
'''

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