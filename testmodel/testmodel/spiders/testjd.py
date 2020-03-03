# -*- coding: utf-8 -*-
import scrapy
import json

from testmodel.items import TestmodelItem


class TestjdSpider(scrapy.Spider):
    name = 'testjd'
    allowed_domains = ['3.cn']
    start_urls = ['https://dc.3.cn/category/get']

    def parse(self, response):
        result=response.body.decode('GBK')
        datass=json.loads(result)
        # print(type(datas))
        item=TestmodelItem()
        datas=datass['data']
        for data in datas:
            category_info=data['s'][0]
            b_category_info=category_info['n']
            item['b_category_name'],item['b_category_url']=self.get_category_name_url(b_category_info)
            # print('大分类信息：{}'.format(b_category_info))
            #获取中分类信息
            m_category_list=category_info['s']
            for m_category in m_category_list:
                m_category_info=m_category['n']
                # print('中分类信息：{}'.format(m_category_info))
                item['m_category_name'], item['m_category_url'] = self.get_category_name_url(m_category_info)
                #获取小分类信息
                s_category_list=m_category['s']
                for s_category in s_category_list:
                    s_category_info=s_category['n']
                    # print('小分类信息：{}'.format(s_category_info))
                    item['s_category_name'], item['s_category_url'] = self.get_category_name_url(s_category_info)
                    # print(item)
                    yield item
    def get_category_name_url(self,category_info):
        """
        信息数据分三类：
            1.i-list.jd.com/list.html?cat=14065,14099,14104|手部防护||0
            2.9855-9859-9926|开关插座||0
            3.1713-3271|旅游地图||0
        :param category_info:
        :return: category_name,category_url
        """
        #1.i-list.jd.com/list.html?cat=14065,14099,14104|手部防护||0
        category_info_list = category_info.split('|')
        category_name = category_info_list[1]
        if category_info_list[1].count('jd.com'):


            category_url='https://'+category_info_list[0]
            #3.1713-3271|旅游地图||0
            #https://item.jd.com/11327594.html
        elif category_info_list[1].count('-')==1:
            category_url='https://channel.jd.com/{}.html'.format(category_info_list[0])
        #2.9855-9859-9926|开关插座||0
        else:
            s=category_info_list[0].replace('-',',')
            category_url='https://list.jd.com/list.html?cat={}'.format(s)
        return category_name,category_url

