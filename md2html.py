#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  only use python markdown module convert markdown to html

'''

import sys
import os
import re
import markdown

if len(sys.argv) > 1:
    lang = sys.argv[-1]
else:
    lang='zh'

def main():
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    ins = re.compile(r'\s*Insert\s+(\d+fig\d+).png')
    for root,dirs,files in os.walk(lang):
        for name in files:
            if name.endswith('.markdown'):
                fn = os.path.join(root, name)
                if not os.path.isdir('tmp/%s' % root):
                    os.makedirs('tmp/%s' % root)
                f1 = open(fn, 'r')
                f2 = open('tmp/%s' % fn, 'w')
                for line in f1:
                    matches = ins.match(line)
                    if matches:
                        n = 'figures/%s-tn.png' % matches.group(1)
                        line = "![%s](%s)\n" % (n, n)
                    f2.write(line)
                f1.close()
                f2.close()
                markdown.markdownFromFile(
                    input=f2.name, 
                    output='%s-%s.html' % (lang, name))
                print '-> %s-%s.html' % (lang, name)

if __name__ == '__main__':
    main()
