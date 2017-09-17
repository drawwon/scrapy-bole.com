#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/8 16:57

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", 'crawl', 'jobbole'])
