# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # 主播名称
    nickname = scrapy.Field()
    # 房间名称
    room_name = scrapy.Field()
    # 人气
    hot = scrapy.Field()
    # 房间号
    room_id = scrapy.Field()
    # 主播标签
    tag = scrapy.Field()
