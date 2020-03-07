# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
import json
from jsonpath import jsonpath

from dishonest.items import DishonestItem

"""
完善爬虫：
步骤：
    1.起始
    2.生成所有页面的请求
    3.解析页面，提取需要的数据
爬虫出现Forbidden by robots.txt:关闭scrapy自带的ROBOTSTXT_OBEY功能，在setting找到这个变量，设置为False即可解决。
"""


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信人&pn=10&rn=10&ie=utf-8&oe=utf-8']

    def parse(self, response):
        datas=json.loads(response.text)
        #获取总条数
        #disp_Num=jsonpath(results,'$..dispNum')[0]
        # print('数据总条数',disp_Num)
        # disp_data=jsonpath(results,'$..disp_data')这是错误的，网页上显示的不一定是对的，真实打印出来是result
        results=jsonpath(datas,'$..result')[0]
        for result in results:
            print(type(result))
            item=DishonestItem()
            item['name']=result['iname']
            # 失信人员名
            # 失信人号码
            item['card_num']=result['cardNum']
            # 失信人年龄
            item['age']=int(result['age'])
            # 区域
            item['area']=result['areaName']
            # 法人（企业）
            item['business_entity']=result['businessEntity']
            # 失信内容
            item['content']=result['duty']
            # 公布日期
            item['publish_date']=result['publishDate']
            # 公布/执行单位
            item['publish_unit']=result['courtName']
            # 创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(item)
            #把数据交给引擎
            yield item
        #获取总页数
        # list_Num=2

