# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

from .settings import MONGODB_URL
from .spiders.testjd import TestjdSpider


class TestmodelPipeline(object):
    def open_spider(self,spider):
        if isinstance(spider,TestjdSpider):
            #爬虫启动之后链接数据库
            self.client=MongoClient(MONGODB_URL)
            #获取数据库中的集合
            self.collections=self.client['jd']['test']
    #向数据库中添加数据,将item转换成字典
    def process_item(self, item, spider):
        if isinstance(spider, TestjdSpider):
            self.collections.insert_one(dict(item))
        return item

    def close_spider(self,spider):
        if isinstance(spider, TestjdSpider):
            self.client.close()
