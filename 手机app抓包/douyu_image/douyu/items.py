# -*- coding: utf-8 -*-

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    #照片名字
    nickname = scrapy.Field()
    # 照片路径
    imagelink = scrapy.Field()
    # 照片保存路径
    imagePath = scrapy.Field()
