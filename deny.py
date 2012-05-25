#!/usr/bin/env python
#coding:utf-8

import re
flag1 = re.I|re.S

def replace_pattern(pattern1,s1,count1 = None):
    re_cpl = re.compile(pattern1,flag1)#python 2.6
    if count1 is None:
        return re.sub(re_cpl,'',s1)
    else:
        return re.sub(re_cpl,'',s1,count1)

def replace_base_tag(s1,count1 = 1):
    pattern1 = r'<\s*base\W.+?>'
    return replace_pattern(pattern1,s1,count1)
    
def replace_iframe(s1):
    pattern1 = r'<\s*iframe.*?\Wiframe\s*>'
    return replace_pattern(pattern1,s1)

def replace_js_plus(s1):
    pattern1 = r'''<\s*script.*?<\s*/\s*script\s*>'''
    return replace_pattern(pattern1,s1)

def replace_googleplus_hide(s1):
    pattern1 = '''<style>\s*body\s*{[^{}]*?visibility\s*:\s*hidden\s*;\s*}\s*</style>'''
    return replace_pattern(pattern1,s1)

def replace_on_load(s1):
    load_pattern = '''<[^>]+?(onload\s*=\s*(?P<pt1>['"])[^>]+?(?P=pt1))[^>]*?>'''
    iter1 = re.finditer(load_pattern,s1,flag1)
    new_str = ''
    pos = 0
    for each in iter1:
        try:
            before_pos = each.start(1)
            after_pos = each.end(1)
            new_tag = s1[each.start():before_pos] +\
                s1[after_pos:each.end()]
            new_str += s1[pos:each.start()] + new_tag
            pos = each.end()
        except:
            continue
    new_str += s1[pos:]
    return new_str

def replace_all_plus(s1,nojs = None):#todo,make pattern match once
    s1 = replace_base_tag(s1)
    s1 = replace_iframe(s1)
    if nojs is not None:
        s1 = replace_js_plus(s1)
    s1 = replace_on_load(s1)
    s1 = replace_googleplus_hide(s1)
    return s1

