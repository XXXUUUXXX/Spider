# -*- coding: utf-8 -*-

import pymongo
from .items import ZhihuItem,RelationItem,AnswerItem,ArticleItem,QuestionItem


class ZhihuPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                mongo_uri = crawler.settings.get('MONGO_URI'),
                mongo_db = crawler.settings.get('MONGO_DATABASE','zhihu')
            )
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    # 调用对应的item
    # isinstance(a,b)函数判断一个对象是否是一个已知类型(a为b类型)
    def process_item(self, item, spider):
        if isinstance(item, ZhihuItem):
            self._process_user_item(item)
        elif isinstance(item, AnswerItem):
            self._process_answer_item(item)
        elif isinstance(item, QuestionItem):
            self._process_question_item(item)
        elif isinstance(item, ArticleItem):
            self._process_article_item(item)
        else:
            self._process_relation_item(item)
        return item

    # self.db.表名.insert(dict(item))创建表，存放数据
    # 用户表
    def _process_user_item(self, item):
        self.db.User.insert(dict(item))

    # 关系表
    def _process_relation_item(self, item):
        try:
            isnext, relation_type = item['relation_type'].split(':')
            if isnext == 'next':
                for one in item['relations_id']:
                    # 修改器$push向数据中添加新的数据
                    #{$push:{filed:value}}中的field应为数组类型的，如果field不是数组类型的，就会出错，如果filed不存在，则创建该数组类型并插入数据，而$pushAll是向数据中添加数组数据
                    self.db.Relation.update({'user_id': item['user_id'], 'relation_type': relation_type}, {'$push': {'relations_id': one}})
        except:
            self.db.Relation.insert(dict(item))

    # 回答表
    def _process_answer_item(self, item):
        self.db.Answer.insert(dict(item))

    # 提问表
    def _process_question_item(self, item):
        self.db.Question.insert(dict(item))

    # 文章表
    def _process_article_item(self, item):
        self.db.Article.insert(dict(item))