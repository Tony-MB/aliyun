import requests
import json
import re
import js2py#用于破解加密技术
#url='http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg=110000'
#解析cookies
"""
#每一个cookies都绑定了一个IP地址和User-Agent
确定cookies来源：响应首部 Set-Cookie 被用来由服务器端向客户端发送 cookie：HttpOnly;secure;
1.__jsluid_h：第一次请求服务器（521），服务器设置的
2.SECTOKEN：第二次请求服务器设置的
3.__jsl_clearance：通过js生成的


"""
index_url='http://www.gsxt.gov.cn/corp-query-entprise-info-xxgg-100000.html'
headers={
 # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

}
#获取request的session对象，可以自动合并cookies的信息
session=requests.session()

#使用session发送请求
response=session.get(index_url,headers=headers)
print(response.status_code)
# print(response.content.decode())
#1.提取script标签中的js
js=re.findall('<script>(.+?)</script>',response.content.decode())[0]
#2.由于这种加密js，最终指向的js代码，都是在eval函数中的，所有‘{eval（’替换成{code=（，其中code可以是其他名称
js=js.replace('{eval(','{code=(')

# print(js)
#3.获取要执行的js
#3.1 获取执行js环境
context=js2py.EvalJs()#使用js2py.eval_js()获得<script></script>中的某一个变量的值，并转换为python中的字典
context.execute(js)#打印code的值
# print(context.code)
#打印code的值
# print(context.code)
#获取cookies的js
cookie_code=re.findall("document.(cookie=.+)\+';Expires",context.code)[0]
# print(cookie_code)
print('------------------------------')
#执行js，获取cookies信息
context.execute(cookie_code)
#打印cookies
print(context.cookie)#__jsl_clearance=1583741695.4|0|btF3xusXZ0y7afrvlfOR8VdYu8I%3D
#var _1f=[function(_2n){return _2n},function(_1f){return _1f},function(_2n){return eval('String.fromCharCode('+_2n+')')},
# function(_2n){for(var _1f=0;_1f<_2n，这些js2py不能使用
#在js2py中，是不能使用document，window这些浏览器对象,但这次发现数据里没有这些信息，所以不需要把document替换


# #打印code的值
# # print(context.code)#<RequestsCookieJar[<Cookie __jsluid_h=ec2357ab0d8a2a588abd1fe1f863969a for www.gsxt.gov.cn/>]>第一个cookies信息

"""
cookie='__jsl_clearance=1583737752.92|0|'+(function(){var _1f=[function(_2n){return _2n},function(_1f){return _1f},
function(_2n){return eval('String.fromCharCode('+_2n+')')},function(_2n){for(var _1f=0;_1f<_2n.length;_1f++){_2n[_1f]=parseInt(_2n[_1f]).toString(36)};return _2n.join('')}],_2n=[[(-~-~{}+[])+[~~'']],[[(-~[]+[2])/[2]]+[-~((-~-~{})*[(-~[]<<(-~{}<<-~{}))])]],'Vuu1J',[[(+!+{})]+[-~-~{}+(-~~~''+[-~-~{}]>>-~-~{})]],[[-~[[-~-~{}]*((-~~~''+[-~-~{}]>>-~-~{}))]]+[(-~[]<<(-~{}<<-~{}))]],[{}+[]][0].charAt(-~~~''+(-~~~''+[((-~{}<<-~{})<<-~{})]>>-~~~'')),[[-~[3+(-~{}<<-~{})+(-~{}<<-~{})]]+
[(+!+{})]],[((-~-~{}^-~[])+[]+[[]][0])+[(-~[]<<(-~{}<<-~{}))]],'dn',


"""

# headers={
#  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
#  'Cookie':'__jsluid_h=7d60e76944af273c14de574aa7e6f318; __jsl_clearance=1583729452.76|0|C7ZKyy0ke4yt5akRo%2FRsyfCRxVc%3D; SECTOKEN=7035424802304953450;'
# }
#
# data={
#     # 'draw':'3',
#     'start':'20',
#     'length':'10'
# }





















# response=requests.post(url,data=data,headers=headers )
# print(response.status_code)#不加cookies状态吗是521
# print(response.text)