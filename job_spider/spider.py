# -*- coding:utf-8 -*-

import requests
import time
import re
import json
import random
import logging
from lxml import etree


class SpiderMeta(type):
    """爬虫类的元类，注册子类到列表，爬虫类指定此元类才能加入进程"""

    spiders = []
    def __new__(mcs, name, bases, attrs):
        mcs.spiders.append(type.__new__(mcs, name, bases, attrs))
        return type.__new__(mcs, name, bases, attrs)


class BaseSpider(object):
    """爬虫类的基类，提供属性和方法"""

    # 职位和城市，运行指定的参数会赋值实例属性
    job = 'Python'
    city = '北京'

    headers = {
        'Connection':'keep-alive'
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        'Accept':'application/json, text/javascript, */*; q=0.01'
        'Accept-Encoding':'gzip, deflate, br'
        'Accept-Language':'zh-CN,zh;q=0.9'
    }
    logger = logging.getLogger('root')
    # 同一爬虫连续请求的最短间隔
    request_sleep = 5
    # 用于记录最近一次请求的时间戳
    _time_recode = 0

    def request(self, method='get', url=None, encoding=None, **kwargs):
        """
        根据爬虫类重新封装的'requests'，可保持请求间隔，并带有默认头部
        method: 请求方法，'get'或'post'
        url: 请求链接
        encoding: 指定对返回对象进行编码
        kwargs: 其他requests自带的参数
        return: Response对象
        """
        
        # 没有指定头部则使用默认头部
        if not kwargs.get('headers'):
            kwargs['headers'] = self.headers
        # 随机生成系数对间隔产生变化
        # random.uniform(a,b)：用于生成一个指定范围内的随机浮点数，两格参数中，其中一个是上限，一个是下限
        rand_multi = random.uniform(0.8, 1.2)
        # 距离上次请求的间隔
        interval = time.time() - self._time_recode