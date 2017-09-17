#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/10 20:58
import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    print(get_md5('http://jobbole.com'))

