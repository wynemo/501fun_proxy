#!/usr/bin/env python
#coding:utf-8
def handle_damn_tco(s1):
    import re
    rule = r'(?<=content="0;URL[=])\S+?(?=")'
    object1 = re.search(rule,s1,re.S|re.X|re.I)
    if object1:return object1.group()
    else:return None
    
