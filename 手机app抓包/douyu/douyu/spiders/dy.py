# -*- coding: utf-8 -*-
import scrapy

import json
from douyu.items import DouyuItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DySpider(scrapy.Spider):
    name = 'dy'
    allowed_domains = ['apiv2.douyucdn.cn']
    
    page = 0
    url_first = 'https://apiv2.douyucdn.cn/gv2api/rkc/roomlist/2_270/'
    url_last = '/20/android?client_sys=android'
    url = url_first + str(page) + url_last
    #start_urls = [url]

    # 解决HTTP status code is not handled or not allowed
    def start_requests(self):  
        yield scrapy.Request(self.url, headers={'User-Agent': "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"})  

    def parse(self, response):
        data = json.loads(response.text)['data']
        # 解决TypeError: list indices must be integers, not str，某些主播没有标签
        try:
            list = data['list']
            for each in list:
                item = DouyuItem()
                # 主播名称
                item['nickname'] = each['nickname']
                # 房间名称
                item['room_name'] = each['room_name']
                # 人气
                item['hot'] = each['hn']
                # 房间号
                item['room_id'] = each['room_id']
                # 主播标签
                for i in each['anchor_label']:
                    item['tag'] = i['tag']
                yield item
        except:
            pass

        self.page += 20
        yield scrapy.Request(self.url_first + str(self.page) + self.url_last, callback = self.parse)

