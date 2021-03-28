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
    title_num_str = title.split('.')[0]
    # print(codeText)
    eng_title = ''
    hpp_title = 'q'
    for i in range(4 - len(title_num_str)):
        hpp_title += '0'
    hpp_title += title_num_str + '_'
    # print(codeText)
    if codeText.find('Solution') != -1:
        eng_title = codeText.split('(')[0].split(' ')[-1]
        hpp_title += eng_title + '.hpp'
        # 写入.hpp文件
        hpp_text = '#include"tools.hpp"\n'
        hpp_text += codeText.replace('};', '')
        hpp_text += '\n    void test(){\n        std::cout<<"test start"<<std::endl;\n    }\n};'
    else:
        eng_title = codeText.split('\nclass ')[1].split(' {')[0]
        hpp_title += eng_title + '.hpp'
        # 写入.hpp文件
        hpp_text = '#include"tools.hpp"\n'
        hpp_text += codeText
        hpp_text += 'class Solution {\npublic:\n    void test(){\n        std::cout<<"test start"<<std::endl;\n    }\n};'

    hpp_text = add_std(hpp_text)
    # 判断是否已经存在文件，如果有就不改了
    if not os.path.exists(folder_path + '/include/' + hpp_title):
        print('hpp')
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

    # 文档部分
    note_name = hpp_title.split('.')[0] + '.html'
    with open(folder_path + '/notes/' + note_name, 'w', encoding='utf-8')as html_f:
        html_f.write('<p>' + title + '</p>\n\n')
        html_f.write(qContent)
    note_name = note_name.split('.')[0] + '.md'
    with open(folder_path + '/notes/' + note_name, 'w', encoding='utf-8')as md_f:
        md_f.write('# ' + title + '\n')
        md_f.write(html2md(qContent))
    os.startfile(folder_path + '/notes/' + note_name)
