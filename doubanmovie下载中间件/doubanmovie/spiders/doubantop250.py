# -*- coding: utf-8 -*-
import scrapy
from doubanmovie.items import DoubanmovieItem

class Doubantop250Spider(scrapy.Spider):
    name = 'doubantop250'
    allowed_domains = ['movie.douban.com']
    offset = 0
    url = 'https://movie.douban.com/top250?start='
    end = '&filter='
    start_urls = [url + str(offset) + end]

    def parse(self, response):
        item = DoubanmovieItem()
        movies = response.xpath('//div[@class="info"]')
        for each in movies:
            # 标题
            item['title'] = each.xpath('.//span[@class="title"]/text()').extract()[0]
            # 信息
            item['bd'] = each.xpath('.//div[@class="bd"]/p/text()').extract()[0]
            # 评分
            item['star'] = each.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            # 简介
            item['quote'] = each.xpath('.//div[@class="bd"]//span[@class="inq"]/text()').extract()

            yield item

        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url + str(self.offset) + self.end, callback = self.parse)
