# -*- coding: utf-8 -*-

import scrapy
import json
from douyu.items import DouyuItem


class DouyumeinvSpider(scrapy.Spider):
    name = "douyumeinv"
    allowed_domains = ["capi.douyucdn.cn"]

    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 将json中的data转换为python,data是列表
        data = json.loads(response.text)['data']
        for each in data:
            item = DouyuItem()
            item['nickname'] = each['nickname']
            item['imagelink'] = each['vertical_src']

            # 将数据交给管道文件
            yield item
        if self.offset < 1000:
            self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback = self.parse)
