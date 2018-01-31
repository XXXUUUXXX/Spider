# -*- coding: utf-8 -*-
import scrapy

import re
import json
import time

#from scrapy.http import Request
from ..items import ZhihuItem, RelationItem, AnswerItem, QuestionItem, ArticleItem
from ..scrapy_redis.spiders import RedisSpider


class ZhihuspiderSpider(RedisSpider):
    name = 'zhihuspider'
    redis_key = 'zhihuspider:start_urls'
    #allowed_domains = ['www.zhihu.com']
    #start_urls = ['http://www.zhihu.com/']
    start_user_id = ['yun-he-shu-ju-8','miao-bi-xiao-xian']

    def start_requests(self):
        for one in self.start_user_id:
            # meta参数的作用是传递信息给下一个函数，meta只接受字典类型的赋值
            # meta = {'key1': value1, 'key2': value2}
            # 在下一个函数中取出value1，只需得到上一个函数的meta['key1']即可
            # 因为meta是随着Request产生是传递的，下一个函数得到的Response对象中就会有meta
            # 即response.meta  取value1则是value1 = response.meta['key1']
            yield scrapy.Request('https://www.zhihu.com/api/v4/members/'+one+'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics', meta={'user_id':one}, callback=self.parse)

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
        # 有多个地点返回列表，若用户没有填写，返回空列表
        item['locations'] = []
        for i in dict_result['locations']:
            item['locations'].append(i['name'])

        # 所在行业
        # 可能有用户没有填写，使用异常机制，若business中没有则在industry_category中查找，还没有则为空
        try:
            item['business'] = dict_result['business']['name']
        except:
            try:
                item['business'] = dict_result['industry_category']
            except:
                pass

        # 职业经历
        # 创建空列表，异常判断返回公司：工作
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
        # 创建空列表，异常判断返回学校：专业
        item['education'] = []
        for i in dict_result['educations']:
            try:
                educations = i['school']['name'] + ':' + i['major']['name']
            except:
                try:
                    educations = i['school']['name']
                except:
                    pass
            item['education'].append(educations)

        # 关注人数
        item['followees_num'] = dict_result['following_count']

        # 粉丝人数
        item['followers_num'] = dict_result['follower_count']

        yield item

        item = RelationItem()
        # start_requests返回的用户id
        one = response.meta['user_id']
        # 关系人的id
        item['relations_id'] = []
        # 用户id
        item['user_id'] = one
        # 关系类型(关注了，关注者)
        item['relation_type'] = ''
        # 粉丝
        yield scrapy.Request('https://www.zhihu.com/api/v4/members/'+one+'/followers?include=data[*].answer_count,badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_relation,meta={'item':item,'offset':0,'relation_type':'followers'})
        # 关注
        yield scrapy.Request('https://www.zhihu.com/api/v4/members/'+one+'/followees?include=data[*].answer_count,badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_relation,meta={'item':item,'offset':0,'relation_type':'followees'})
        # 回答
        yield scrapy.Request('https://www.zhihu.com/api/v4/members/'+one+'/answers?include=data[*].comment_count,content,voteup_count,created_time,updated_time;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_answer,meta={'answer_user_id':one,'offset':0})
        # 提问
        yield scrapy.Request('https://www.zhihu.com/people/'+one+'/asks?page=1',callback=self.parse_question,meta={'ask_user_id':one,'page':1})
        # 文章
        yield scrapy.Request('https://www.zhihu.com/api/v4/members/'+one+'/articles?include=data[*].comment_count,content,voteup_count,created,updated;data[*].author.badge[?(type=best_answerer)].topics&limit=20&offset=0',callback=self.parse_article,meta={'author_id':one,'offset':0})


    def parse_relation(self, response):
        json_result = str(response.body, encoding='utf8').replace('false','0').replace('true', '1')
        dict_result = eval(json_result)

        # 关系人列表
        relations_id = []
        for one in dict_result['data']:
            relations_id.append(one['url_token'])
        response.meta['item']['relations_id'] = relations_id

        if response.meta['offset'] == 0:
            response.meta['item']['relation_type'] = response.meta['relation_type']
        else:
            response.meta['item']['relation_type'] = 'next:' + response.meta['relation_type']
        yield response.meta['item']

        # 进入关系人主页获取信息
        for one in response.meta['item']['relations_id']:
            yield scrapy.Request('https://www.zhihu.com/api/v4/members/'+one+'?include=locations,employments,industry_category,gender,educations,business,follower_count,following_count,description,badge[?(type=best_answerer)].topics',meta={'user_id':one},callback=self.parse)
        
        # 有后续页面则offset+20
        if dict_result['paging']['is_end'] == 0:
            offset = response.meta['offset'] + 20
            # 正则匹配URL
            next_page = re.findall('(.*offset=)\d+', response.url)[0]
            yield scrapy.Request(next_page + str(offset), callback = self.parse_relation, meta = {'item': response.meta['item'], 'offset': offset, 'relation_type': response.meta['relation_type']})

    def parse_answer(self, response):
        json_result = str(response.body, encoding='utf8').replace('false', '0').replace('true', '1')
        dict_result = eval(json_result)

        for one in dict_result['data']:
            item = AnswerItem()
            # 回答的用户
            item['answer_user_id'] = response.meta['answer_user_id']
            # 回答内容的id
            item['answer_id'] = one['id']
            # 问题的id
            item['question_id'] = one['question']['id']
            # 创建的时间
            # item['cretated_time'] = one['created_time']
            time_c = one['created_time']
            item['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_c))
            # 更新的时间
            #item['updated_time'] = one['updated_time']
            time_u = one['updated_time']
            item['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_u))
            # 赞成数量
            item['voteup_count'] = one['voteup_count']
            # 评论数量
            item['comment_count'] = one['comment_count']
            # 回答内容
            item['content'] = one['content'].replace('<p>','').replace('</p>','')
            yield item

        if dict_result['paging']['is_end'] == 0:
            offset = response.meta['offset'] + 20
            next_page = re.findall('(.*offset=)\d+', response.url)[0]
            yield scrapy.Request(next_page + str(offset), callback = self.parse_answer, meta = {'answer_user_id': response.meta['answer_user_id'], 'offset': offset})

    def parse_question(self, response):
        # 用xpath提取提问页面信息
        data = response.xpath('//div[@class="List-item"]')
        for one in data:
            item = QuestionItem()
            # 提问人的id
            item['ask_user_id'] = response.meta['ask_user_id']
            # 提问标题
            item['title'] = one.xpath('.//a/text()').extract()[0]
            # 问题的id
            item['question_id'] = one.xpath('.//a/@href').extract()[0].replace('/question/','')
            # 提问时间
            item['ask_time'] = one.xpath('.//span/text()').extract()[0]
            # 回答数量
            item['answer_count'] = one.xpath('.//span/text()').extract()[1]
            # 关注数量
            item['followees_count'] = one.xpath('.//span/text()').extract()[2]
            yield item

        # 翻页
        next_page = response.xpath('//button[@class="Button PaginationButton PaginationButton-next Button--plain"]/text()').extract()
        if next_page:
            response.meta['page'] += 1
            next_url = re.findall('(.*page=)\d+', response.url)[0] + str(response.meta['page'])
            yield scrapy.Request(next_url, callback = self.parse_question, meta = {'ask_user_id': response.meta['ask_user_id'], 'page': response.meta['page']})

    def parse_article(self, response):
        json_result = str(response.body, encoding = 'utf8').replace('false', '0').replace('true', '1')
        dict_result = eval(json_result)

        for one in dict_result['data']:
            item = ArticleItem()
            # 作者id
            item['author_id'] = response.meta['author_id']
            # 文章标题
            item['title'] = one['title'] 
            # 文章id
            item['article_id'] = one['id']
            # 内容
            item['content'] = one['content']
            # 创建时间
            time_c = one['created']
            item['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_c))
            # 更新时间
            time_u = one['updated']
            item['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_u))
            # 赞成数量
            item['voteup_count'] = one['voteup_count']
            # 评论数量
            item['comment_count'] = one['comment_count'] 
            yield item

        if dict_result['paging']['is_end'] == 0:
            offset = response.meta['offset'] + 20
            next_page = re.findall('(.*offset=)\d+', response.url)[0]
            yield scrapy.Request(next_page + str(offset), callback = self.parse_article, meta = {'author_id': response.meta['author_id'], 'offset': offset})

