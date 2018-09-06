# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ZufangPipeline(object):
    def __init__(self):
        self.filename = open('zufang.json','a',encoding='utf8')
    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.filename.write(content)
        return item

    def spider_closed(self,spider):
        self.filename.close()