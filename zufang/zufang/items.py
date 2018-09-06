# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # define the fields for your item here like:
    #房屋地址
    address = scrapy.Field()
    #面积
    acreage = scrapy.Field()
    #格局
    pattern = scrapy.Field()
    #租金
    rent = scrapy.Field()
    #出租方式
    rentstyle = scrapy.Field()
    #装修
    decorate = scrapy.Field()
    #分数
    score = scrapy.Field()

    url = scrapy.Field()

