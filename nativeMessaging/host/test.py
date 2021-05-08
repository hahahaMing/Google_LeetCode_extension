#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 22:37
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : test.py

import json
import os
import re

# folder_path = 'E:/self_study/git/Google_LeetCode_extension/test_cmake'
folder_path = 'E:/self_study/git/cmake_demo'
src_path = folder_path + '/src'
CML_path = folder_path + '/CMakeLists.txt'

cpp_title = 'q0091_numDecodings.cpp'
# os.system('cd E:\self_study\git\cmake_demo && code . && code src/q0091_numDecodings.cpp')
# os.system('cd '+folder_path+' && code . && code src/'+cpp_title)
import subprocess
subprocess.check_call('code .',cwd='E:\self_study\git\cmake_demo')