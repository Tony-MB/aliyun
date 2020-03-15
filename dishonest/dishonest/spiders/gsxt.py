# -*- coding: utf-8 -*-
import json
import re

import scrapy

from dishonest.items import DishonestItem

"""
失信人公告每次请求成功,都需要携带cookies信息,并且一个cookies信息要和一个user-agent和代理ip绑定,才能请求成功
如果一个cookies请求过于频繁的话,会被限制.
步骤:
    创建爬虫
    修改原来的随机爬虫user-agent,和随机代理的下载器中间类,如果是公示系统的话爬虫直接跳过
    实现专门用于处理公示系统爬虫cookies的中间件
    完善爬虫
"""

class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    start_urls = ['http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html']
    #失信企业公告信息地区的url
    data_url='http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg={}'
    def parse(self, response):
        # print(response.status)
        # print
        #   获取包含省或者直辖市的名称和id,div列表
        divs=response.xpath("//div[@class='label-list']/div")
        for div in divs:
            area=div.xpath('./label/text()').extract_first()
            id=div.xpath('./@id')
            data_url=self.data_url.format(id)
            for i in range(0,50,10):
                data ={
                    'start':str(i),
                    'lenght':'10'
                }
                yield scrapy.FormRequest(data_url,formdata=data,callback=self.parse_data,meta={'area':area})

    def parse_data(self,response):
        #取出传递过来的区域
        area=response['area']
        #把json格式字符串,转换为字典
        result=json.loads(response.text)
        #获取公告信息
        datas=result['data']
        #遍历datas,获取给一个公告信息
        for data in datas:
            item=DishonestItem()
            #获取通知标题
            notice_title=data['noticeTitle']
            #获取通知内容
            notice_content=data['noticeContent']
            #失信人名称
            names=re.findall("关?于?将?(.+?)的?列入.*",notice_title)
            item['name']=names[0] if len(names) !=0 else ''
            name_card_num=re.findall("")


