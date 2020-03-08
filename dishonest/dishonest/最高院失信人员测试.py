import requests
url='http://jszx.court.gov.cn/api/front/getPublishInfoPageList'
headers={

'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',

}
data={
'pageSize': 10,
'pageNo': 1
}
res=requests.post(url,data=data,headers=headers)
print(res.status_code)
print(res.text)#可以打印出完整的数据