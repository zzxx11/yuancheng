# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dnSpider.items import DnspiderItem

class ZgcSpider(CrawlSpider):
    name = 'zgc'
    # allowed_domains = ['detail.zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/notebook_index/subcate16_list_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'list/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = DnspiderItem()
        # item['brand'] = response.xpath(".//div[@id='J_BrandAll']/a/@href").extract()
        # name = response.xpath(".//div[@id='J_BrandAll']/a/font/text()").extract()

        # for i in name:
        #     print(i)
        pass