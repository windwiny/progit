#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  Use python markdown module convert markdown to html

'''

import sys
import os
import re
import markdown


INDEX = '''<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
    <title>Pro Git</title>
  </head>
  <frameset cols="20%,80%">
    <frame src="directory.html">
    <frame name="content"src="ch1-0.html">
    <noframes>
      <body>
      <p>This page uses frames. The current browser you are using does not support frames.</p>
      </body>
    </noframes>
  </frameset>
</html>'''

DIRECTORY = '''<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
    <title>Pro Git</title>
    <style> a { font-size: 0.8em;}; </style>
  </head>
  <body>
    %s
  </body>
</html>'''

HTML = '''<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
    <title>%s</title>
    <link rel=stylesheet type="text/css" href="../epub/master.css">
  </head>
  <body>
    <div id="wrapper">
    <div id="content">
    %s
    </div>
    </div>
  </body>
</html>
'''

def writefile(filename, txt):
    if type(txt) == type(u''):
        txt = txt.encode('utf-8')
    if os.path.isfile(filename) and open(filename, 'r').read() == txt:
        print ' -> %s  \t some as old, skip ..' % filename
    else:
        open(filename, 'w').write(txt)
        print ' -> %s' % filename

def md2html(lang):
    htmldir = 'html_%s' % lang
    if not os.path.isdir(htmldir):
        os.mkdir(htmldir)

    charpter, section = 1, 0
    htmlfiles = []
    for root, dirs, files in os.walk(lang):
        for name in files:
            if name.endswith('.markdown'):
                src = os.path.join(root, name)

                data = open(src, 'r').read()
                # replace image
                data = re.sub(r'\s*Insert\s+(\d+fig\d+).png',
                              r"![figures/\1-tn.png](../figures/\1-tn.png)\n",
                              data,
                              re.IGNORECASE)

                # markdown text to html text
                htmltxt = markdown.markdown(data.decode('utf-8')).encode('utf-8')

                # split charpter section
                for body in htmltxt.split('<h2>'):
                    body = '<h2>' + body
                    title = re.search(r'<h(\d)>(.*?)</h\1>', body).groups()[1]
                    dst = '%s/ch%d-%d.html' % (htmldir, charpter, section)
                    htmlfiles.append((dst, title, charpter, section))
                    txts = HTML % (title, body)
                    writefile(dst, txts)
                    section += 1
                charpter += 1
                section = 0

    # create directory.html
    htmllinks = []
    for fn, title, ch, se in htmlfiles:
        fn = os.path.split(fn)[1]
        if se == 0:
            htmllinks.append('<b><a href="%s" target="content">%d %s</a></b><br />' % (fn, ch, title))
        else:
            htmllinks.append('&nbsp;&nbsp;<a href="%s" target="content">%d.%d %s</a><br />' % (fn, ch, se, title))
    writefile('%s/directory.html' % htmldir, DIRECTORY % '\n'.join(htmllinks))

    # create index.html
    writefile('%s/index.html' % htmldir, INDEX)

def main(langs):
    for lang in langs:
        print '%s\nGenerating %s html files\n%s' % ('--' * 30, lang, '--' * 30)
        md2html(lang)

if __name__ == '__main__':
    langs = []
    if len(sys.argv) > 1:
        for d in sys.argv[1:]:
            if os.path.isdir(d):
                langs.append(d)

    if langs:
        main(langs)
    else:
        print 'Syntax:\n  %s langdir [langdir ..] ' % os.path.basename(sys.argv[0])
