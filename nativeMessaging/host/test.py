#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 22:37
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : test.py

import json

with open('test.json',encoding='utf-8')as fp:
    data = json.load(fp)
    print(data['title'])