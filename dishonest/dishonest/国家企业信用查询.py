import requests
url='http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg=110000'


#UM_distinctid=170ba81c970306-02f08654667898-31760856-1fa400-170ba81c971615; __jsluid_h=34f6f057fa788dadf66498aa35c60af3; SECTOKEN=7035420604284800072;

headers={
#'Cookie':'UM_distinctid=170ba81c970306-02f08654667898-31760856-1fa400-170ba81c971615; __jsluid_h=34f6f057fa788dadf66498aa35c60af3; __jsl_clearance=1583755770.432|0|rN8FbqBcvPyt%2Bm6wex6wbMB5nmM%3D; ',
#'Cookie':'UM_distinctid=170ba81c970306-02f08654667898-31760856-1fa400-170ba81c971615; __jsluid_h=34f6f057fa788dadf66498aa35c60af3; SECTOKEN=7035420604284800072;__jsl_clearance=1583743250.513|0|tNUqz%2BH%2BRvxlbEUj8WrSxZLQM%2F0%3D;',
 #'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
 # 'Cookie':'__jsluid_h=7d60e76944af273c14de574aa7e6f318; __jsl_clearance=1583729452.76|0|C7ZKyy0ke4yt5akRo%2FRsyfCRxVc%3D; SECTOKEN=7035424802304953450;'
#'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
#'Cookie': '__jsluid_h=34f6f057fa788dadf66498aa35c60af3; SECTOKEN=7035420604284800072; __jsl_clearance=1583745685.541|0|kr5BHpACbzI0cnX%2BQcz8GV107xo%3D;',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
'Cookie': 'UM_distinctid=170ba81c970306-02f08654667898-31760856-1fa400-170ba81c971615; __jsluid_h=34f6f057fa788dadf66498aa35c60af3; SECTOKEN=7035420604284800072; __jsl_clearance=1583845763.061|0|1dnB5tezcZHDe8%2F07xqQd8cdVxM%3D; CNZZDATA1261033118=978414828-1583731453-http%253A%252F%252Fwww.gsxt.gov.cn%252F%7C1583844877; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1583845802; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=1583845802; JSESSIONID=3DB782A4F82242593411F9289A12D899-n2:2; tlb_cookie=S172.16.12.132',
}
#__jsl_clearance=1583743250.513|0|tNUqz%2BH%2BRvxlbEUj8WrSxZLQM%2F0%3D;
data={
    # 'draw':'3',.
    'start':'30',
    'length':'10'
}
# response=requests.post(url,data=data,headers=headers)
session=requests.session()
response=session.post(url,headers=headers)
print(response.status_code)
print(response.text)
