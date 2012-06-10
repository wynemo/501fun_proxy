#!/usr/bin/env python
# coding: utf-8

import web
from config import settings
import convert_link
import deny
import util
import tco
import urllib2

render = settings.render
std_headers = settings.std_headers

class proxy:
    def GET(self,para):
        import re
        import base64
        import urllib
        from StringIO import StringIO
        import gzip
        import zlib

        def my_direct(url):
            server_port = web.ctx.env.get('SERVER_PORT',80)
            x_server_port = web.ctx.env.get('HTTP_X_FORWARDED_PROTO','http')
            if('443' == server_port or 'https' == x_server_port):
                raise web.seeother("https://" + web.ctx.host + url)
            else:
                raise web.seeother(url) 

        def set_len_header(len1 = None):
            if i1.headers.has_key('Content-Length'):
                if len1:
                    web.header('Content-Length',len1,unique=True)
                else:
                    web.header('Content-Length',i1.headers['Content-Length'],
                        unique=True)
                    
        def is_html(type1):
            if type1 is not None and len(type1):
                return -1 != type1.lower().find('text/html')
            return False
            
        def redirect_refresh(url):
            new_url = tco.find_meta_refresh_url(s2)
            if(new_url and len(new_url)):
                url1 = '/proxy?url=' + util.my_quote_plus(new_url)
                if nojs is not None:
                    url1 += '&nojs=1'
                set_len_header()
                my_direct(url1)#303

        def r1(p1,str1):
            o1 = re.search(p1,str1)
            if o1 is not None:
                return o1.group(1)
            return None

        def get_character_set(s1):
            def_char = 'utf-8'
            p_str = r'<\s*meta[^<>]+?charset\s*=\s*(\S+)[^<>]*?>'
            p1 = re.compile(p_str,re.I|re.S)
            char_set = r1(p1,s1)
            f = lambda x : x.replace('"','').replace("'",'').strip()
            return def_char if char_set is None else f(char_set)

        def redirect_sharp(url):
            url_part_o = re.search(r'(.+)(#.*)',url)
            if url_part_o is not None:
                url1 = '/proxy?url=' + util.my_quote_plus(url_part_o.group(1))
                if nojs is not None:
                    url1 += '&nojs=1'
                url1 += url_part_o.group(2)
                my_direct(url1)#303

        i = web.input()
        b64 = None
        nojs = None
        url = None
        rf = None
        if web.url().startswith('/proxy') == False:
            rf = web.ctx.env.get('HTTP_REFERER', None) 
            if rf is None:
                raise web.notfound()
            proxy_refer_pattern = r'https?://' + web.ctx.host + r'/proxy[?].*?url=(.+)'
            proxy_url_o = re.match(proxy_refer_pattern,rf)
            if proxy_url_o is not None:
                un_url = urllib.unquote(proxy_url_o.group(1))
                url = r1(r'(\w+://(?:[^/]+\.)+[^/]+)',un_url)
                rf = url
                url = url + para
            else:
                raise web.notfound()
        try:
            if url is None:
                url = i.url.strip()
        except:pass

        agent = web.ctx.env.get('HTTP_USER_AGENT', '').lower()
        if url is None:
            mobile = None
            if agent.find('android') != -1 or\
                agent.find('iphone') != -1 or\
                agent.find('ipad') != -1:
                mobile = 1
            return render.proxy(mobile)

        url = util.replace_amp(url)

        try:nojs = i.nojs
        except:pass

        try:b64 = i.b64
        except:pass

        try:
            if rf is None:
                rf = i.rf
        except:pass

        if b64 == '1':
            url = urllib.unquote_plus(base64.b64decode(url))
        redirect_sharp(url) 

        
        header1 = std_headers.copy()
        header1['User-Agent'] = web.ctx.env.get('HTTP_USER_AGENT', header1['User-Agent'])
        #request = urllib2.Request(url.encode('utf-8'), None, header1)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        opener.addheaders = [('User-agent', header1['User-Agent'])] #todo
        if rf:
            #request.add_header('Referer',rf)
            opener.addheaders.append(('Referer',rf))
        try:
            #i1 = urllib2.urlopen(request,timeout = 3)
            i1 = opener.open(url.encode('utf-8'),timeout = 3)
            redirect_sharp(i1.url) 
        except Exception,e:
            return str(e)
                
        s2 = i1.read()
        if i1.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(s2)
            f = gzip.GzipFile(fileobj=buf)
            s2 = f.read()
        elif i1.info().get('Content-Encoding') == 'deflate':
            try:
                s2 = zlib.decompress(s2)
            except:
                s2 = zlib.decompressobj(-zlib.MAX_WBITS).decompress(s2)
        #get content type
        content_type = None
        if i1.headers.has_key('Content-Type'):
            content_type = i1.headers['Content-Type']
            if content_type and len(content_type):
                web.header('Content-Type',content_type, unique=True)
               
        #image     
        type1 = i1.headers.type
        pt1 = util.picType(type1)
        if pt1:
            set_len_header()
            return s2

        char_set = get_character_set(s2)#get character set,default utf-8
        
        #css
        if type1.lower().endswith('css'):
            s2 = convert_link.convert_html_tag_url(s2,i1.url,None,nojs,char_set)
            set_len_header(str(len(s2)))
            return s2
        
        #if has meta refresh pattern,303
        redirect_refresh(url)
            
        if is_html(content_type) or\
            re.search(r'<\s*html',s2,re.S|re.I):#should be html
            #deny
            s2,base_url = deny.replace_all_plus(s2,nojs)
            #conver href,src in tag
            s2 = convert_link.convert_html_tag_url(s2,i1.url,base_url,nojs,char_set)
            
            set_len_header(str(len(s2)))
            return s2
        else:
            #other type
            set_len_header()
            return s2
