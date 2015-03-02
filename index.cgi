#!/path/to/python3.4
# -*- coding: utf-8 -*-


import cgi
import cgitb
import io
import os
import re
import sys
from collections import defaultdict

class Page:
    def __init__(self):
        self.__q = {k: v[0] for k, v in cgi.parse_qs(os.environ['QUERY_STRING']).items()}
        q = self.__q

        # filter page reference
        if 'page' not in q:
            q['page'] = 'home'
        if re.search(r'[^a-z_]', q['page']):
            q['page'] = ''
        
        self.__data = ['<p>Page not found.</p>']
        self.__opts = defaultdict(lambda: None)

        if q['page']:
            path = 'docs/pages/' + q['page'] + '.dat'
            if os.path.exists(path):
                lines = [x.strip('\n') for x in open(path, encoding='UTF-8').readlines()]
                n = 0
                while n < len(lines):
                    l = lines[n]
                    if not l or l[0] != '#':
                        break
                    ls = l[1:].split('=')
                    self.__opts[ls[0]] = ls[1]
                    n += 1
                self.__data = lines[n:]

    def write_http_header(self):
        print('Content-Type: text/html; charset=UTF-8')
        print()

    def make_page_header(self):
        doc = []
        doc.append('<!DOCTYPE html>')
        doc.append('<html lang="ja">')
        doc.append('<head>')
        doc.append('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">')
        doc.append('<meta http-equiv="Content-Style-Type" content="text/css">')
        doc.append('<meta http-equiv="Content-Script-Type" content="text/javascript">')
        doc.append('<link rel="stylesheet" href="styles/common.css" type="text/css">')
        
        if self.__opts['title']:
            doc.append('<title>' + self.__opts['title'] + ' | Site Name</title>')
        else:
            doc.append('<title>Site Name</title>')
        doc.append('</head><body>')
        doc.append('<header><h1>Site Name</h1></header>')

        if self.__opts['nav']:
            navstr = ' &gt; '.join('<a href="/?page=%s">%s</a>' % (x, x) for x in self.__opts['nav'].split('/'))
            doc.append('<nav><p>' + navstr + '</p></nav>')

        return doc

    def make_page_footer(self):
        doc = []
        doc.append('<footer><p>Copyright (C) 20XX- by Your Name. All rights reserved.</p></footer>')
        doc.append('</body>')
        doc.append('</html>')
        return doc

    def make_page_content(self):
        return self.__data

    def write_page(self):
        doc = []
        doc += self.make_page_header()
        doc += self.make_page_content()
        doc += self.make_page_footer()
        
        for text in doc:
            try:
                print(text)
            except Exception as ex:
                print('<p>' + str(ex) + '</p>')
        
        
def main():
    cgitb.enable()
    try:
        page = Page()
        page.write_http_header()
        page.write_page()
    except Exception as ex:
        raise ex
        print('Content-Type: text/html; charset=UTF-8')
        print()
        print(ex)
        
    

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    main()
