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
        for one in self.start_user_id:
            yield Request('https://www.zhihu.com/api/v4/members/' + one +'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics',meta={'user_id':one},callback=self.parse)

    def parse(self, response):
        json_result = str(response.body,encoding='utf8').replace('false', '0').replace('true', '1')
        # eval将字符串str当成有效的表达式来求值并返回计算结果
        dict_result = eval(json_result)

        item = ZhihuItem()
        # 用户id
        item['user_id'] = dict_result['url_token']
        # 用户头像链接
        item['user_image_url'] = dict_result['avatar_url'][:-6] + 'x1.jpg'
        # 用户名
        item['name'] = dict_result['name']
        # 性别
        if dict_result['gender'] == 1:
            item['gender'] = '男'
        elif dict_result['gender'] == 0:
            item['gender'] = '女'
        else:
            item['gender'] = '未知'
        # 居住地
        item['locations'] = []
        for i in dict_result['locations']:
            item['locations'].append(i['name'])
        # 所在行业
        try:
            item['business'] = dict_result['business']['name']
        except:
            try:
                item['business'] = dict_result['industry_category']
            except:
                pass
        # 职业经历
        item['employments'] = []
        for i in dict_result['employments']:
            try:
                employment = i['company']['name'] + ':' + i['job']['name']
            except:
                try:
                    empolyment = i['company']['name']
                except:
                    pass
            item['employments'].append(employment)
        # 教育经历
        item['educations'] = []
        for i in dict_result['educations']:
            try:
                educations = i['school']['name'] + ':' + i['major']['name']
            except:
                try:
                    educations = i['school']['name']
                except:
                    pass
            item['educations'].append(educations)

        # 关注人数
        item['followees_num'] = dict_result['following_count']
        # 粉丝人数
        item['followers_num'] = dict_result['follower_count']
        yield item

        item = RelationItem()
        one = response.meta['user_id']
        # 用户id
        item['user_id'] = one
        # 关系类型
        item['relation_type'] = ''
        # 关系人的id
        item['relations_id'] = []
        # yield Request('')


    def parse_relation(self, response):
        json_result = str(response.body, encoding='utf8').replace('false','0').replace('true', '1')
        dict_result = eval(json_result)
        relations_id = []
