# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zufang.items import ZufangItem
import re

'''两周之内   完成下面小项目：
租房网站上爬取租房信息，筛选出适合我们自己租赁的房屋信息.
要求：
1、获取房屋地址、面积、格局、租金、装修情况等信息
2、去重复房屋信息
3、房屋筛选，去掉中介信息、去除分数过低房源、选择整租合租等
4、去除数据异常值（租金过高或者过低，要找适合自己的）
5、如有可能，根据上班地点和自身条件，重新给房源评分，最终找到适合自己的房源'''

class ZfSpider(CrawlSpider):
    name = 'zf'
    allowed_domains = ['sz.zu.fang.com']
    # start_urls = ['http://sz.zu.fang.com/']
    # pagelink = LinkExtractor(allow=("/house/i\d+"))
    # link = LinkExtractor(allow=("/chuzu/\d+"))

    start_urls = ['http://sz.zu.fang.com/hezu/']
    pagelink = LinkExtractor(allow=("/hezu/i\d+"))
    link = LinkExtractor(allow=("/hezu/\d+"))

    rules = (
        Rule(pagelink, callback='parse_item', follow=True),
        Rule(link,callback='parse_link',follow=True)
    )

    def parse_item(self, response):
        # i = ZufangItem()
        print(response.url)
        # lst = response.xpath('//dl[@class="list hiddenMap rel"]/dd/p[1]/a/@title').extract()
        # for i,lt in enumerate(lst):
        #     print(i,lt)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i

    def parse_link(self,response):
        print(response.url)
        print(response.request.headers)
        item = ZufangItem()
        item['address'] = self.get_address(response)
        item['acreage'] = self.get_acreage(response)
        item['pattern'] = self.get_pattern(response)
        item['rent'] = self.get_rent(response)
        item['rentstyle'] = self.get_rentstyle(response)
        item['decorate'] = self.get_decorate(response)
        item['score'] = self.get_score(response)
        item['url'] = response.url
        return item

    def get_rent(self,response):
        rent = response.xpath('//div[@class="trl-item sty1"]/i/text()').extract()
        return rent[0] if len(rent) else 'null'

    def get_rentstyle(self,response):
        rentstyle = response.xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[1]/div[1]/text()').extract()

        return rentstyle[0] if len(rentstyle) else 'null'

    def get_pattern(self,response):
        pattern = response.xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[2]/div[1]/text()').extract()
        return pattern[0] if len(pattern) else 'null'

    def get_acreage(self,response):
        acreage = response.xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[3]/div[1]/text()').extract()
        return acreage[0] if len(acreage) else 'null'

    def get_decorate(self,response):
        decorate = response.xpath('/html/body/div[5]/div[1]/div[2]/div[4]/div[3]/div[1]/text()').extract()
        return decorate[0] if len(decorate) else 'null'

    def get_address(self,resonse):
        addr = resonse.xpath('//*[@id="agantzfxq_C01_02"]/text()').extract()[0] +  resonse.xpath('//*[@id="agantzfxq_C01_03"]/text()').extract()[0]
        addr = re.sub('租房','',addr)
        address = resonse.xpath('/html/body/div[5]/div[1]/div[2]/div[5]/div[2]/div[2]/a/text() | /html/body/div[5]/div[1]/div[2]/div[5]/div[3]/div[2]/a/text()').extract()

        return addr+address[0]

    def get_score(self,response):
        score = response.xpath('//div[@class="pj-sec clearfix rel"]/div[1]/span[2]/text()').extract()[0]
        return score