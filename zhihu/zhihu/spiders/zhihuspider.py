# -*- coding: utf-8 -*-
import scrapy

import re
import json
#import pdb
#from scrapy.http import Request
from zhihu.items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem
from scrapy_redis.spiders import RedisSpider


class ZhihuspiderSpider(RedisSpider):
    name = 'zhihuspider'
    redis_key = 'zhihuspider:start_urls'

    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #start_user_id = ['peng-dong-cheng-38']


    def start_requests(self):
        for one in self.start_user_id:
            # meta参数的作用是传递信息给下一个函数，meta只接受字典类型的赋值
            # meta = {'key1': value1, 'key2': value2}
            # 在下一个函数中取出value1，只需得到上一个函数的meta['key1']即可
            # 因为meta是随着Request产生是传递的，下一个函数得到的Response对象中就会有meta
            # 即response.meta  取value1则是value1 = response.meta['key1']
            yield scrapy.Request('https://www.zhihu.com/api/v4/members/' + one +'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics',meta={'user_id':one},callback=self.parse)

    def parse(self, response):
        # 将response(json)转换成字符串型，并替换其中的false和true
        json_result = str(response.body,encoding='utf8').replace('false', '0').replace('true', '1')
        # eval函数用来做数据类型的转换,eval将字符串型的list,tuple,dict转变成原有的类型(数据还原成它本身)
        dict_result = eval(json_result)

        item = ZhihuItem()
        # 用户id
        item['user_id'] = dict_result['url_token']
        # 用户头像链接，
        # 对原头像链接切片https://pic3.zhimg.com/v2-3dcd43d154a55b32c1b3ccb8103e6777_is.jpg
        # is.jpg显示小图，x1.jpg显示大图https://pic3.zhimg.com/v2-3dcd43d154a55b32c1b3ccb8103e6777_x1.jpg
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
