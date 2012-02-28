#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  Use python markdown module convert markdown to html

'''

import sys
import os
import re
import markdown

langs = ['zh']
if len(sys.argv) > 1:
    for d in sys.argv[1:]:
        if os.path.isdir(d):
            langs.append(d)

html = '''
<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type">
    <title>%(title)s</title>
    <link rel=stylesheet type="text/css" href="./epub/master.css">
  </head>
  <body>
    <div id="wrapper">
    <div id="content">
    %(body)s
    </div>
    </div>
  </body>
</html>
'''

def md2html(lang):
    ins = re.compile(r'\s*Insert\s+(\d+fig\d+).png')
    for root,dirs,files in os.walk(lang):
        for name in files:
            if name.endswith('.markdown'):
                src = os.path.join(root, name)
                dst = '%s-%s.html' % (lang, name)
                if os.path.isfile(dst) and '-f' not in sys.argv and os.stat(dst).st_mtime > os.stat(src).st_mtime:
                    print "%s newer %s, skip.. \t(or add '-f' param)" % (dst, src)
                    continue
                if not os.path.isdir('tmp/%s' % root):
                    os.makedirs('tmp/%s' % root)
                f1 = open(src, 'r')
                f2 = open('tmp/%s' % src, 'w')
                for line in f1:
                    matches = ins.match(line)
                    if matches:
                        n = 'figures/%s-tn.png' % matches.group(1)
                        line = "![%s](%s)\n" % (n, n)
                    f2.write(line)
                f1.close()
                f2.close()

                title = dst
                body = markdown.markdown(open(f2.name,'r').read().decode('utf-8')).encode('utf-8')
                open(dst, 'w').write(html % locals())
                print '-> %s' % dst
    
def main():
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    for lang in langs:
        print '%s\nGenerating %s html files\n%s' % ('--' * 30, lang, '--' * 30)
        md2html(lang)

if __name__ == '__main__':
    main()
