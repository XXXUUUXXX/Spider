# -*- coding: utf-8 -*-
import scrapy

import re
import json
import pdb
from scrapy.http import Request
from zhihu.items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem
from scrapy_redis.spiders import RedisSpider


class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuspider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #start_user_id = ['un-he-shu-ju-8']


    def start_requests(self):
        for i in self.start_user_id:
            yield Request('https://www.zhihu.com/api/v4/members/' + i +'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics',meta={'user_id':one},callback=self.parse)

    def parse(self, response):
        json_result = str(response.body,encoding='utf8').replace('false', '0').replace('true', '1')
        # eval将字符串str当成有效的表达式来求值并返回计算结果
        dict_result = eval(json_result)

        item = ZhihuItem()
        if dict_result['gender'] == 1:
            item['gender'] = '男'
        elif dict_result['gender'] == 0:
            item['gender'] = '女'
        else:
            item['gender'] = '未知'
        item['user_id'] = dict_result['url_token']
        item['user_image_url']