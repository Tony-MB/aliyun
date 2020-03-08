# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
import json

from dishonest.items import DishonestItem


class CourtSpider(scrapy.Spider):
    name = 'court'
    allowed_domains = ['court-gov.cn']
    #start_urls = ['http://court-gov.cn/']
    post_url='http://jszx.court.gov.cn/api/front/getPublishInfoPageList'

    #构建起始请求
    def start_requests(self):
        data = {
        'pageSize': '10',
        'pageNo': '1',
        }
        #构建post请求交给引擎
        yield scrapy.FormRequest(self.post_url,formdata=data,callback=self.parse)

    def parse(self, response):
        results=json.loads(response.text)
        #print(results)
        #获取总页数
        page_count=results['pageCount']
        # print('总页数',page_count)
        #构建每一个请求,实现翻页
        for page in range(page_count):
            data = {
                'pageSize': '10',
                'pageNo': str(page),
            }
            #yield scrapy.FormRequest(self.post_url,formdata=data,callback=self.parse)爬虫会自动停止
            #dont_filter = True，# 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
            yield scrapy.FormRequest(self.post_url,formdata=data,dont_filter = True ,callback=self.parse_page)#到这一步就运行不了了

    def parse_page(self,response):
        print('解析数据')
        results = json.loads(response.text)
        # print(results)
        #获取失信人信息列表
        datas=results['data']
        print(len(datas))
        for data in datas:
            # print(data)
            item=DishonestItem()
            item['name'] = data['name']
            # 失信人员名
            # 失信人号码
            item['card_num'] = data['cardNum']
            # 失信人年龄
            item['age'] = data['age']
            # 区域
            item['area'] = data['areaName']
            # 法人（企业）
            item['business_entity'] = data['buesinessEntity']
            # 失信内容
            item['content'] = data['duty']
            # 公布日期
            item['publish_date'] = data['publishDate']
            # 公布/执行单位
            item['publish_unit'] = data['courtName']
            # 创建日期
            item['create_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 更新日期
            item['update_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(item)
            # 把数据交给引擎
            yield item



