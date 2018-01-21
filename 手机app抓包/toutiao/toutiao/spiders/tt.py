# -*- coding: utf-8 -*-
import scrapy

import json
from toutiao.items import ToutiaoItem


class TtSpider(scrapy.Spider):
    name = 'tt'
    allowed_domains = ['snssdk.com']

    page = 0
    # 抓包获取的头条评论api地址
    url = 'https://lf.snssdk.com/article/v2/tab_comments/?group_id=6513100048023159299&offset='
    start_urls = [url + str(page)]

    def parse(self, response):
        # 转换为python格式
        data = json.loads(response.text)['data']
        for c in data:
            item = ToutiaoItem()
            each = c['comment']
            # 用户名称
            item['name'] = each['user_name']
            #评论内容
            item['content'] = each['text']
            # 点赞数量
            item['digg_count'] = each['digg_count']
            # 回复数量
            item['reply_count'] = each['reply_count']

            yield item

        self.page += 20
        yield scrapy.Request(self.url + str(self.page), callback = self.parse)


