#from util import get_base_url
import util
import re

flag1 = re.I|re.S
pre1 = '/proxy?url='


def convert_html_tag_url(s1,refer_url,nojs=None,charset='utf-8'):
    def get_current(url):
        pos = url.rfind('/')
        if pos != -1:
            return url[:pos]
        return url
    def convert_rel_url(path1,ref_url):
        rv = ref_url
        pos = rv.rfind('/')
        if pos != -1:
            rv = rv[:pos]
        while 1:
            if path1.startswith('../'):
                path1 = path1[3:]
                rv = get_current(rv)
            else:
                break
        return rv + '/' + path1
    def convert_url(url):
        if url.startswith('#'):
            return url
        elif url.startswith('//'):#for links starts with '//',this link is same with the page's crx protocol
            url = 'http:' + url
        elif not url.startswith('http'):
            if url.startswith('/'):
                url = util.get_base_url(refer_url) + url
            elif url.startswith('..'):
                url = convert_rel_url(url,refer_url)
            else:
                url = get_current(refer_url) + '/' + url
        f = lambda x: '' if x is None else '&nojs=1'
        url = util.get_chs_lnk(url,charset)
        return ''.join([pre1,util.my_quote_plus(url),f(nojs)])
    #p1 = r'''(?:<\s*\w+\s+[^>]*?(?:\shref|\ssrc)\s*=\s*["']?\s*([^>'"\s]+)(?=\s*["']?[^>]*?>))'''
    p1 = r'''(?:(?:\Whref|\Wsrc)\s*=\s*["']?\s*([^>'"\s]+)(?=\s*["']?[^>]*?>))'''
    p2 = r'''(?:url\s*[(]\s*['"]?([^)]+?)['"]?\s*[)])'''#see dbanotes.net 
    #p2 before url should be \s todo
    p3 = r'''(?:[(]\s*src\s*=\s*["']?([^)]+?)["']?\s*[)])'''
    p4 = r'''(?:<\s*(?:object|param)\s+[^>]*?(?:data|value)\s*=\s*["']?\s*([^>'"\s]+)(?=\s*["']?[^>]*?>))'''
    #example:@import '1510_layout.css'; from http://my1510.cn/templates/skin3/css/1510.css
    p5 = r'''(?:@import\s+["']([^"']+?)["']\s*;)'''
    pt = p1 + '|' +p2 + '|' + p3 + '|' + p4 + '|' + p5
    iter1 = re.finditer(pt,s1,flag1)
    new_str = ''
    pos = 0
    for each in iter1:
        try:
            if each.group(1):
                url_index = 1
            elif each.group(2):
                url_index = 2 
            elif each.group(3):
                url_index = 3
            elif each.group(4):
                url_index = 4
            else:
                url_index = 5
            before_pos = each.start(url_index)
            after_pos = each.end(url_index)
            new_url = each.group(url_index)
            if not new_url.startswith('data:'):
                new_url = convert_url(new_url)
                new_url += '&rf=' + util.my_quote_plus(refer_url)
            #print 'new_url is',new_url
            new_tag = s1[each.start():before_pos] +\
                new_url +\
                s1[after_pos:each.end()]
            new_str += s1[pos:each.start()] + new_tag
            pos = each.end()
        except Exception,e:
            print str(e)
            continue
    new_str += s1[pos:]
    return new_str

#convert urls in css
def conver_url_in_css(s1):
    return s1

