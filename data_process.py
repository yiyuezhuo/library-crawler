# -*- coding: utf-8 -*-
"""
Created on Sun May 22 21:27:10 2016

@author: yiyuezhuo
"""

import json
import os

from main2 import Entry,MaxiterBreak,check
from collections import Counter
from itertools import chain
from render import render

with open('test.json','r') as f:
    dic=json.load(f)
    

def monitor_gen(gen):
    def _gen(*args,**kwargs):
        #print(1)
        __gen=gen(*args,**kwargs)
        def ___gen():
            for i,res in enumerate(__gen):
                print(i)
                yield res
        #print(2)
        return ___gen()
    return _gen
    
def to_cache(func):
    # func return a string
    def _func():
        pass
    return _func

    
@monitor_gen
def html_iter(dic,bind_path='data'):
    for username in dic.values():
        path=os.path.join(bind_path,username+'.html')
        with open(path,encoding='utf8') as f:
            html=f.read()
        yield username,html
    
def scan(dic,bind_path='data'):
    if not(os.path.isdir(bind_path)):
        os.mkdir(bind_path)
    for username in dic.values():
        path=os.path.join(bind_path,username+'.html')
        if os.path.exists(path):
            print('pass {} -> {}'.format(username+'.html',bind_path))
            continue
        state='succ'
        entry=Entry(username)
        try:
            entry.get_login()
        except MaxiterBreak:
            state='fail'
            #print('MaxiterBreak raise')
        res=entry.get_history_head()
        with open(path,'wb') as f:
            f.write(res.content)
        print('{} {} -> {}'.format(state,username+'.html',bind_path))
        
def get_history(check_d,bind_path='history'):
    if not os.path.isdir(bind_path):
        os.mkdir(bind_path)
    for username,check_dic in check_d.items():
        if check_dic['type'] in ['onepage','multiple']:
            path=os.path.join(bind_path,username+'.json')
            if os.path.exists(path):
                print('pass {} history -> {}'.format(username,bind_path))
                continue
            entry=Entry(username)
            try:
                rd=entry.process()
            except MaxiterBreak:
                print('fail {} history -!-> {}'.format(username,bind_path))
                continue
            with open(path,'w') as f:
                json.dump(rd,f)
            print('succ {} history -> {}'.format(username,bind_path))
            
            
def load_cache(check_d_path='check_d.json',history_path='history'):
    with open(check_d_path) as f:
        check_d=json.load(f)
    history_d={}
    for name in os.listdir(history_path):
        path=os.path.join(history_path,name)
        print('load {}'.format(path))
        _id,suffix=name.split('.')
        with open(path) as f:
            history_d[_id]=json.load(f)
    return {'check_d':check_d,'history_d':history_d}
    
        
def intergration(check_d,history_d):
    records=check_d.copy()
    for _id,check_dic in check_d.items():
        if check_dic['type'] in ['onepage','multiple']:
            if _id in history_d:
                records[_id]['history']=history_d[_id]['history']
            else:
                records[_id]['history']=[]
                records[_id]['type']=records[_id]['type']+' fail'
        else:
            records[_id]['history']=[]
    return records
    
#download(dic)
if __name__=='__main__':
    '''
    with open('check_d.json') as f:
        check_d=json.load(f)
    get_history(check_d)
    '''
    with open('records.json') as f:
        records=json.load(f)