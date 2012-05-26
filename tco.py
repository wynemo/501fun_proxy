#!/usr/bin/env python
#coding:utf-8
def handle_damn_tco(s1):
    import re
    rule = r'(?<=content="0;URL[=])\S+?(?=")'
    object1 = re.search(rule,s1,re.S|re.X|re.I)
    if object1:return object1.group()
    else:return None

def find_meta_refresh_url(s1):
    import re
    p1 = re.compile(r'''<\s*meta.+?http-equiv="refresh".*?>''',re.I|re.S)
    p2 = re.compile(r'''content\s*=\s*(?P<quote>["'])0;URL=(\S+?)(?P=quote)''',re.I|re.S)
    o1 = re.search(p1,s1)
    if o1 is None:
        return None
    o2 = re.search(p2,o1.group())
    if o2 is None:
        return None
    url = o2.group(2)
    if url is None:
        return None
    return url.replace("'",'').replace('"','').strip()
