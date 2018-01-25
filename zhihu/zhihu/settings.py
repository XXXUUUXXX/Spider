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
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用了scrapy-redis里的调度器组件，不使用scrapy默认的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 允许暂停，redis请求记录不会丢失
SCHEDULER_PERSIST = True
# 队列形式，请求先进先出
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"


# 指定数据库的主机IP
REDIS_HOST = "127.0.0.1"
# 指定数据库的端口号
REDIS_PORT = 6379
# 多台主机部署分布式爬虫时，在REDIS_URL中填入连接redis的主机URL
REDIS_URL = None


# 主机名
MONGODB_HOST = '127.0.0.1'
# 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DNNAME = 'zhihu'
# 存放数据的表名称
#MONGODB_SHEETNAME = ''


DOWNLOADER_MIDDLEWARES = {
    zhihu.middlewares.ProxyMiddleware': 100,
    zhihu.middlewares.UserAgentMiddleware': 200,
    zhihu.middlewares.CookiesMiddleware': 300,
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

