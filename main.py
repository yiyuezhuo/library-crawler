# -*- coding: utf-8 -*-
"""
Created on Sun May 22 19:03:10 2016

@author: yiyuezhuo
"""

import requests
import random
import webbrowser

def fff(res,temp_path='temp.html'):
    if type(res)!=str:
        res=res.content#.decode('utf8')
    with open(temp_path,'wb') as f:
        f.write(res)
    webbrowser.open(temp_path)

url1='http://202.115.193.41:8080/opac/login?locale=zh_CN'
url2='http://202.115.193.41:8080/pages/include/checklogin.jsp'
url4='http://202.115.193.41:8080/opac/mylibrary'
url5='http://202.115.193.41:8080/opac/mylibrary/circulationHistory'

img_url_root='http://202.115.193.41:8080/code/'

data={'username':'2014010199','password':'010199','loginType':'barCode','kaptcha':'C'}

headers1_s='''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:en,zh-CN;q=0.8,zh;q=0.6
Connection:keep-alive
Host:202.115.193.41:8080
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'''

headers2_s='''Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:en,zh-CN;q=0.8,zh;q=0.6
Connection:keep-alive
Content-Type:application/x-www-form-urlencoded
Host:202.115.193.41:8080
Origin:http://202.115.193.41:8080
Referer:http://202.115.193.41:8080/opac/login?locale=zh_CN
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36
X-Requested-With:XMLHttpRequest'''

headers_img_s='''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:en,zh-CN;q=0.8,zh;q=0.6
Connection:keep-alive
Host:202.115.193.41:8080
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'''

def parseHeaders(headers_s):
    dic={}
    for line in headers_s.split('\n'):
        index=line.index(':')
        key=line[:index]
        value=line[index+1:]
        dic[key]=value
    return dic
    
headers1=parseHeaders(headers1_s)
#del headers1['Cookie']

headers2=parseHeaders(headers2_s)
#del headers2['Cookie']

headers_img=parseHeaders(headers_img_s)

data={'username':'2014060801',
      'password':'060801',
      'loginType':'barCode',
      'kaptcha':'A'}


def entry(data):
    session=requests.session()
    res1=session.get(url1,headers=headers1)
    res2=session.get(img_url_root,headers=headers_img)
    res3=session.post(url2,data=data,headers=headers2)
    #res2=session.get(img_url_root)
    #res3=session.post(url2,data=data)
    #return {'res1':res1,'res2':res2,'res3':res3}
    return {'res1':res1,'res2':res2,'res3':res3,'session':session}
    
    
'''
res=requests.post(url,data=data)

res_l=[]
for i in range(100):
    res=requests.post(url,data=data)
    res_l.append(res)
    print(res.content.decode('utf8'))
'''
res_l=[]

for i in range(20):
    _data=data.copy()
    _data['kaptcha']=random.choice(['A','B','C','D'])
    res_dic=entry(_data)
    res_l.append(res_dic)
    print(res_dic['res3'].content.decode('utf8'))