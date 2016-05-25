# -*- coding: utf-8 -*-
"""
Created on Wed May 25 13:10:24 2016

@author: yiyuezhuo
"""

import jinja2
from main2 import fff

def load_template(fname,tabMap='    '):
    with open(fname,'r',encoding='utf8') as f:
        s=f.read()
    return jinja2.Template(s.replace('\t',tabMap))

template=load_template('render_template.html')

def render(record):
    records=[[his['name'],his['id'],his['date']] for his in record['history'] if his['type']=='借书']
    html=template.render(records=records)
    fff(html)