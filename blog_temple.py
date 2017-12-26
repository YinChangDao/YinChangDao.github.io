#!/usr/local/bin/python3

import datetime
import time
import sys

def print_usage():
    print('usage: blog_temply.py <filename>')

def generate(name):
    now_date = time.strftime("%Y-%m-%d")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    filename = '_posts/{0}-{1}.md'.format(now_date, name)

    text = '''---
layout: post
title:  ""
subtitle: ""
date:   {0} -0400
background: '/img/posts/05.jpg'
---
'''.format(now)

    #print(text)

    print("new file: {0}".format(filename))
    with open(filename, 'w+') as f:
        f.write(text)
        f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
    else:
        generate(sys.argv[1])
