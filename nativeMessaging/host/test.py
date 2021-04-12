#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 22:37
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : test.py

import json
import os
import re

folder_path = 'E:/self_study/git/cmake_demo'
main_path = folder_path + '/main.cpp'


def add_std(s: str) -> str:
    key_words = ['vector', 'string']
    for word in key_words:
        s = s.replace(word, 'std::' + word)
    return s


def html2md(s: str) -> str:
    s = s.replace('\t', '')
    div_dict = re.findall('<div.*>\n', s)
    for pattern in div_dict:
        s = s.replace(pattern, '')
    s = s.replace('</div>\n', '')
    s = s.replace('<p>', '')
    s = s.replace('</p>', '')
    s = s.replace('<code>', "`")
    s = s.replace('</code>', "`")
    s = s.replace('<sub>', "_")
    s = s.replace('</sub>', "")
    s = s.replace('&nbsp;', " ")
    s = s.replace('<strong>', "**")
    s = s.replace('</strong>', "**")
    s = s.replace('<pre>', "")
    s = s.replace('</pre>', "")
    s = s.replace('<ul>\n', "")
    s = s.replace('</ul>', "")
    s = s.replace('<li>', "\n- ")
    s = s.replace('</li>', "")
    s = s.replace('&lt;', "<")
    s = s.replace('<sup>', " ^ ")
    s = s.replace('</sup>', "")
    return s


with open('test.json', encoding='utf-8')as fp:
    data_dic = json.load(fp)
    title = data_dic['title'].encode('utf-8').decode('utf-8')
    qContent = data_dic['qContent'].encode('utf-8').decode('utf-8')
    codeText = data_dic['codeText'].encode('utf-8').decode('utf-8')

    # print(title,qContent,codeText)
    codeText = codeText.replace('\xa0', ' ')
    eng_title = ''
    hpp_title = 'q'
    title_num_str = title.split('.')[0]
    if title.find('面试题') != -1:
        hpp_title = 'm'
        title_num_str = title.split('面试题 ')[1]
        title_num_str = title_num_str.split('.')[0] + title_num_str.split('.')[1]

    for i in range(4 - len(title_num_str)):
        hpp_title += '0'
    hpp_title += title_num_str + '_'
    # print(codeText)
    if codeText.find('Solution') != -1:
        eng_title = codeText.split('Solution')[1].split('(')[0].split(' ')[-1]
        hpp_title += eng_title + '.hpp'
        # .hpp文件文本
        hpp_text = '#include"tools.hpp"\n'
        hpp_text += codeText.replace('};', '')
        hpp_text += '\n    void test(){\n        std::cout<<"test start"<<std::endl;\n    }\n};'
        # 这里加一个测试用例编写
        # 其实就是把括号里的东西逗号改为分号，最后加分号，去掉 “&”
        

        # 定义输入变量（使用初始化函数表）

        # 加一句输出（使用打印函数表）


    else:
        eng_title = codeText.split('\nclass ')[1].split(' {')[0]
        hpp_title += eng_title + '.hpp'
        # .hpp文件文本
        hpp_text = '#include"tools.hpp"\n'
        hpp_text += codeText
        hpp_text += 'class Solution {\npublic:\n    void test(){\n        std::cout<<"test start"<<std::endl;\n    }\n};'
    # 保护函数名类名 同时增加 std::
    hpp_text = hpp_text.replace(hpp_title.split('_')[1].split('.')[0], 'hpp_title')
    hpp_text = add_std(hpp_text)
    hpp_text = hpp_text.replace('hpp_title', hpp_title.split('_')[1].split('.')[0])
    # 判断是否已经存在文件，如果有就不改了
    if not os.path.exists(folder_path + '/include/' + hpp_title):
        with open(folder_path + '/include/' + hpp_title, 'w', encoding='utf-8')as hpp_f:
            hpp_f.write(hpp_text)
    # 修改 main.cpp
    main_text = '#include"' + hpp_title + '"\n'
    with open(main_path, 'r', encoding='utf-8')as main_f:
        old_main_str = main_f.read()
        old_include_len = len(old_main_str.split('\n')[0])
        main_text += old_main_str[old_include_len + 1:]
    with open(main_path, 'w', encoding='utf-8')as main_f:
        main_f.write(main_text)
    # 打开clion
    os.startfile(main_path)
