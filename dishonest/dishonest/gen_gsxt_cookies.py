"""
实现process_request方法,从Redis中随机取出cookies来使用,关闭页面重定向.
实现process_response方法,如果响应码不是200或没有内容重试

实现生成cookies的脚本
    创建gen_gsxt_cookiesl.py在其中创建GenGsxtCookies类
    实现一个方法,用于把一套代理ip,user-agent,cookies绑定到一起的信息放到redis的list中
        随机获取一个user-agent
        随机获取一个代理ip
        获取request的session对象
        把user-agent,通过请求头,设置给session对象
        把代理ip,通过proxies,设置给session对象
        使用session对象,发送请求,获取需要的cookies信息
        把代理ip,user-agent,cookies放到字典中,序列化,存储到redis的list中
    实现一个run方法,用于开启多个异步来执行这个方法


"""
#该pickle模块实现了用于序列化和反序列化Python对象结构的二进制协议。
# “Pickling”是将Python对象层次结构转换为字节流的过程， “unpickling”是反向操作，
# 从而将字节流（来自二进制文件或类似字节的对象）转换回对象层次结构。pickle模块对于错误或恶意构造的数据是不安全的。
import re
import js2py
import pickle
#gevent协程又称为微线程，纤程。英文名Coroutine:协程是一种用户态的轻量级线程
from gevent import monkey

from .settings import USER_AGENTS,REDIS_URL,COOKIES_KEY,COOKIES_USER_AGENT_KEY,COOKIES_PROXY_KEY,REDIS_COOKIES_KEY

monkey.patch_all()
from gevent.pool import Pool
import random
from redis import StrictRedis
import requests
class GenGsxtCookies(object):
    def __init__(self):
        #建立数据库的链接
        self.redis=StrictRedis.from_url(REDIS_URL)
        #创建协程池
        self.pool=Pool()
    #实现一个方法,用于把一套代理ip,user-agent,cookies绑定到一起的信息放到redis的list中
    def push_cookies_to_redis(self):
        #一直执行直到成功
        while True:
            try:
                # 1.随机获取一个user - agent
                user_agent=random.choice(USER_AGENTS)
                # print('随机获取一个user - agent:',user_agent)
                # 2.随机获取一个代理ip,要把代理池的api打开才能使用
                # response=requests.get('http://0.0.0.0:16888/random?protocol=http')
                # proxy=response.content.decode()
                # print('随机获取一个代理ip:',proxy)
                # 3.获取request的session对象
                session=requests.session()
                # 4.把user - agent, 通过请求头, 设置给session对象
                session.headers={
                    'User-Agent':user_agent
                }
                # 5.把代理ip, 通过proxies, 设置给session对象
                proxy='http://116.196.85.166:3128'
                session.proxies={
                    'http':proxy
                }
                print('使用session对象, 发送请求')
                # 6.使用session对象, 发送请求, 获取需要的cookies信息
                index_url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
                response = session.get(index_url)
                # print(response.status_code)
                # print(response.content.decode())
                js = re.findall('<script>(.+?)</script>', response.content.decode())[0]
                # print(js)
                js = js.replace('{eval(', '{code=(')
                # print(js)
                context = js2py.EvalJs()
                context.execute(js)
                # print(context.code)
                cookies_code_list = re.findall(r"document.(cookie=.+)\+';Expires", context.code)
                # print(cookies_code[0])
                cookies_code=cookies_code_list[0]
                print(response.cookies)
                # re.sub是个正则表达式方面的函数，用来实现通过正则表达式，
                # 实现比普通字符串的replace更加强大的替换功能。简单的替换功能可以使用replace()实现。
                # \w 匹配包括下划线的任何单词字符
                # cookies_code=re.sub(r"var\s(\w+)=document.createElement\('\w+'\);\w+.innerHTML='<a href=\\'/\\'>\w+</a>';\w+=\w+.firstChild.href",r"var \1='http://www.gsxt.gov.cn'",cookies_code)
                cookies_code = re.sub(r"var\s(\w+)=document.createElement.+?.firstChild.href",
                                      r"var \1='http://www.gsxt.gov.cn'", cookies_code)
                # print(cookies_code)
                # 执行js,生成我们需要的cookies信息
                context.execute(cookies_code)
                # print(type(context.cookie))
                cookies = context.cookie.split('=')
                # print(cookies)
                session.cookies.set(cookies[0], cookies[1])
                session.get(index_url)
                # 获取cookies字典#  将CookieJar转为字典：从CookieJar中返回一个键/值字典。
                cookies = requests.utils.dict_from_cookiejar(session.cookies)
                print(cookies)
                #7.把代理ip,user-agent,cookies放到字典中,序列化,存储到redis的list中
                cookies_dict={
                    COOKIES_KEY:cookies,
                    COOKIES_USER_AGENT_KEY:user_agent,
                    COOKIES_PROXY_KEY:proxy
                }
                #序列化,存储到redis的list中
                self.redis.lpush(REDIS_COOKIES_KEY,pickle.dumps(cookies_dict))
            except Exception as ex:
                print(ex)

    def run(self):
        for i in range(100):
            self.pool.apply_async(self.push_cookies_to_redis)
        #让主线程等待所有的协程任务完成
        self.pool.join()
if __name__ == '__main__':
    ggc=GenGsxtCookies()
    ggc.push_cookies_to_redis()