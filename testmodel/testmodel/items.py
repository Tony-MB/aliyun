# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestmodelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    b_category_name=scrapy.Field()
    b_category_url = scrapy.Field()
    m_category_name = scrapy.Field()
    m_category_url = scrapy.Field()
    s_category_name = scrapy.Field()
    s_category_url = scrapy.Field()
