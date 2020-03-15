# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests

from .spiders.gsxt import GsxtSpider
from .settings import USER_AGENTS, REDIS_URL

"""
实现随机user-agent下载器
    1.准备user-agent列表
    2.定义RandomUserAgent类
    3.实现process_request方法，设置随机的user-agent
"""
class RandomUserAgent(object):
    def process_request(self,request,spider):
        #如果soider是公示系统爬虫的话,就直接跳过,不用随机产生user-agent
        if isinstance(spider,GsxtSpider):
            return None
        request.headers['User-Agent']=random.choice(USER_AGENTS)
"""
实现ProxyMiddleware类
实现代理ip下载器中间件

"""
class ProxyMiddleware(object):
    #process_request方法，设置代理ip
    def process_request(self,request,spider):
        # 如果soider是公示系统爬虫的话,就直接跳过,不用随机产生user-agent
        if isinstance(spider, GsxtSpider):
            return None
        #1.获取协议头
        protocol=request.url.split('://')[0]
        #2.构建代理ip的请求url
        proxy_url='http://localhost:16888/random?protocol={}'.format(protocol)
        #3.发送请求，获取代理ip
        proxy_url='https://218.75.158.153:3128'
        response=requests.get(proxy_url)
        # 4.把代理匹配设置给request.meta['proxy']
        request.meta['proxy']='https://218.75.158.153:3128'
        return None


"""
#实现公示系统中间类步骤:
    实现process_request方法,从redis中随机取出cookies来使用,关闭页面重定向
    实现process_response方法,如果响应码不是200或者没有内容
Redis Lindex 命令用于通过索引获取列表中的元素。你也可以使用负数下标，以 -1 表示列表的最后一个元素，
 -2 表示列表的倒数第二个元素，以此类推。 
"""
import pickle
from redis import StrictRedis
from .settings import USER_AGENTS,REDIS_URL,COOKIES_KEY,COOKIES_USER_AGENT_KEY,COOKIES_PROXY_KEY,REDIS_COOKIES_KEY
class GsxtMiddleware(object):
    def __init__(self):
        #建立redis数据库链接
        self.redis=StrictRedis.from_url(REDIS_URL)

    def process_request(self,request,spider):
        #从redis中随机取出cookies来使用,关闭页面重定向
        count=self.redis.llen(REDIS_COOKIES_KEY)
        random_index=random.randint(0,count-1)#这个方法[1,2]
        cookie_data=self.redis.lindex(REDIS_COOKIES_KEY,random_index)
        #反序列化,把二进制转换成字典
        cookie_dict=pickle.loads(cookie_data)

        #把cookie信息设置request
        request.headers['User-Agent']=cookie_dict[COOKIES_USER_AGENT_KEY]
        #设置请求代理ip
        request.meta['proxy']=cookie_dict[COOKIES_PROXY_KEY]
        #设置cookies信息
        request.cookies=cookie_dict[COOKIES_KEY]
        # print(request.cookies)
        #设置不要重定向
#from  scrapy.downloadermiddlewares.redirect import RedirectMiddleware
        request.meta['noticeContent']=True

    #如果响应码不是200或者没有内容,重试
    def process_response(self,request,spider,response):
        #如果响应码不是200或者没有内容,重试
        if response.status != 200 or response.body == b'':
            #备份请求
            req=request.copy()
            #设置请求不过滤
            req.dont_filter=True
            #把请求交给引擎
            return req
        return response



