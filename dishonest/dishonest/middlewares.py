# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
from .settings import USER_AGENTS

"""
实现随机user-agent下载器
    1.准备user-agent列表
    2.定义RandomUserAgent类
    3.实现process_request方法，设置随机的user-agent
"""
class RandomUserAgent(object):
    def process_request(self,request,spider):
        request.headers['User-Agent']=random.choice(USER_AGENTS)
"""
实现ProxyMiddleware类
实现代理ip下载器中间件

"""
# class ProxyMiddleware(object):
#     #process_request方法，设置代理ip
#     def process_request(self,request,spider):
#         #1.获取协议头
#         #protocol=request.url.split('://')[0]
#         #2.构建代理ip的请求url
#         # proxy_url='http://localhost:16888/random?protocol={}'.format(protocol)这个需要一个代理池API才嫩而过使用
#         #3.发送请求，获取代理ip
#         # proxy_url='https://218.75.158.153:3128'
#         # response=requests.get(proxy_url)
#         # 4.把代理匹配设置给request.meta['proxy']
#         request.meta['proxy']='https://218.75.158.153:3128'


        # return None
