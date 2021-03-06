# -*- coding: utf-8 -*-

BOT_NAME = 'doubanmovie'

SPIDER_MODULES = ['doubanmovie.spiders']
NEWSPIDER_MODULE = 'doubanmovie.spiders'

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'doubanmovie.middlewares.RandomUserAgent': 100,
    'doubanmovie.middlewares.RandomProxy': 200,
}

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

'''
PROXIES = [
    #{"ip_prot": "219.138.58.109:3128", "user_passwd": "用户名:密码"}
    {"ip_port": "117.158.160.246:9797", "user_passwd": ""},
    {"ip_port": '202.109.207.125:8888', "user_passwd": ""},
    {"ip_port": '223.223.187.195:80', "user_passwd": ""},
]
'''

ITEM_PIPELINES = {
    'doubanmovie.pipelines.DoubanmoviePipeline': 300,
}

# MONGODB主机名
MONGODB_HOST = "127.0.0.1"
#MONGODB端口号
MONGODB_PORT = 27017
#数据库名称
MONGODB_DBNAME = "Douban"
#存放数据的表名称
MONGODB_SHEETNAME = "doubanmovies"

LOG_FILE = "douban.log"
LOG_LEVEL = 'DEBUG'