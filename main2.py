# -*- coding: utf-8 -*-
"""
Created on Sun May 22 20:06:44 2016

@author: yiyuezhuo
"""

import requests
import random
import webbrowser
from bs4 import BeautifulSoup
import re
from itertools import chain


def fff(res,temp_path='temp.html'):
    if type(res)!=str:
        res=res.content#.decode('utf8')
    with open(temp_path,'wb') as f:
        f.write(res)
    webbrowser.open(temp_path)
    
class MaxiterBreak(Exception):
    pass

url_map={
    'checkcode_map_root':'http://202.115.193.41:8080/code/',
    'login_form':'http://202.115.193.41:8080/pages/include/checklogin.jsp',
    'private_main':'http://202.115.193.41:8080/opac/mylibrary',
    'private_history':'http://202.115.193.41:8080/opac/mylibrary/circulationHistory'
}

def htmlOrSoup(func):
    # if pass soup will use soup else transform it to soup
    def _func(arg):
        if type(arg)!=BeautifulSoup:
            soup=BeautifulSoup(arg,'lxml')
        else:
            soup=arg
        return func(soup)
    return _func

class Entry(object):
    def __init__(self,username,password=None):
        if password==None:
            password=username[-6:]
        self.username=username
        self.password=password
        self.session=requests.session()
        self.history=[]
        self.head=None
    def get_form_data(self):
        return {'username':self.username,
                'password':self.password,
                'loginType':'barCode',
                'kaptcha':random.choice(['A','B','C','D'])}
    def get_checkcode(self):
        url=url_map['checkcode_map_root']
        self.session.get(url)
    def try_login(self):
        url=url_map['login_form']
        data=self.get_form_data()
        return self.session.post(url,data=data)
    def get_login(self,maxiter=30):
        for i in range(maxiter):
            self.get_checkcode()
            res=self.try_login()
            print(res.content.decode('utf8'))
            if res.content==b'ok':
                return
        raise MaxiterBreak
    def get_history_head(self):
        #self.session.get(url_map['private_main'])
        return self.session.get(url_map['private_history'])
    def get_history(self,head_res=None):
        if head_res==None:
            head_res=self.get_history_head()
        soup=BeautifulSoup(head_res.content,'lxml')
        head=check(soup)
        self.head=head
        if head['type']=='login fail':
            return []
        elif head['type']=='null':
            return []
        elif head['type']=='onepage':
            self.history=table_extract(soup)
            return self.history
        elif head['type']=='multiple':
            self.history=self.get_history_multiple(head_soup=soup,max_offset=head['max_offset'])
            return self.history
        else:
            raise Exception('unhandle case')
    def get_history_multiple(self,head_soup=None,max_offset=None):
        if head_soup==None:
            head_res=self.get_history_head()
            head_soup=BeautifulSoup(head_res.content)
        if max_offset==None:
            max_offset=check(head_soup)['max_offset']
        
        table_l=[table_extract(head_soup)]
        for offset in range(20,max_offset+20,20):
            url='http://202.115.193.41:8080/opac/mylibrary/circulationHistory?pager.offset={offset}'.format(offset=offset)
            print('get {} offset={}'.format(self.username,offset))
            res=self.session.get(url)
            table=table_extract(res.content)
            table_l.append(table)
        return list(chain(*table_l))
    def process(self):
        self.get_login()
        self.get_history()
        rd=self.head.copy()
        rd['history']=self.history
        return rd
        

@htmlOrSoup
def check(soup):
    #soup=BeautifulSoup(html,'lxml')
    if soup.select_one('#logArea')!=None:
        return {'type':'login fail'}
    al=soup.select_one('#divsubartpage').select('a')
    if len(al)>0:
        href=al[-1].attrs['href']
        max_offset=int(re.search(r'offset=(\d+)',href).groups()[0])
        return {'type':'multiple','max_offset':max_offset}
    tl=soup.select_one('#form1').select('tr')
    if len(tl)>1:
        return {'type':'onepage','times':len(tl)-1}
    else:
        return {'type':'null'}

@htmlOrSoup        
def table_extract(soup):
    record_l=[]
    for tr in soup.select_one('#form1').select('tr')[1:]:
        td_l=tr.select('td')
        record={}
        for i,key in enumerate(['name','id','type','date','fine']):
            record[key]=td_l[i].text.strip()
        record_l.append(record)
    return record_l
    

if __name__ == '__main__':
    entry=Entry('2014060801')
    entry.get_login()
    res=entry.get_history_head()
    #fff(res)
    soup=BeautifulSoup(res.content,'lxml')
    print(check(res.content))

