#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 22:37
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : test.py

import json
import os
import re

folder_path = 'E:/self_study/git/Google_LeetCode_extension/test_cmake'
main_path = folder_path + '/main.cpp'
CML_path = folder_path + 'CMakeList.txt'


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
    s = s.replace('&gt', ">")

    return s


# Helper function that sends a message to the webapp.
def send_message(message):
    print(message)


with open('test.json', encoding='utf-8') as fp:
    data_dic = json.load(fp)
    title = data_dic['title'].encode('utf-8').decode('utf-8')
    qContent = data_dic['qContent'].encode('utf-8').decode('utf-8')
    codeText = data_dic['codeText'].encode('utf-8').decode('utf-8')

    codeText = codeText.replace('\xa0', ' ')
    cpp_title = 'q'
    title_num_str = title.split('.')[0]
    # 修改cmake_list文件以达到使用命名空间的目的
    # 面试题使用 m开头
    if title.find('面试题') != -1:
        send_message('{"text":"m"}')
        cpp_title = 'm'
        title_num_str = title.split('面试题 ')[1]
        title_num_str = title_num_str.split('.')[0] + title_num_str.split(
            '.')[1]
    # 补 0 使编号为 5 个字符
    for i in range(4 - len(title_num_str)):
        cpp_title += '0'
    cpp_title += title_num_str + '_'
    # todo：2021年4月13日看到这，下一步继续改cmake
    if codeText.find('Solution') != -1:
        eng_title = codeText.split('Solution')[1].split('(')[0].split(' ')[-1]
        cpp_title += eng_title + '.hpp'
        # .hpp文件文本
        hpp_text = '#include"tools.hpp"\n'
        hpp_text += codeText.replace('};', '')
        hpp_text += '\n    void test(){\n        std::cout<<"test start"<<std::endl;\n    }\n};'
    else:
        eng_title = codeText.split('\nclass ')[1].split(' {')[0]
        cpp_title += eng_title + '.hpp'
        # .hpp文件文本
        hpp_text = '#include"tools.hpp"\n'
        hpp_text += codeText
        hpp_text += 'class Solution {\npublic:\n    void test(){\n                                        std::cout<<"test start"<<std::endl;\n    }\n};'
    # 保护函数名类名 同时增加 std::
    hpp_text = hpp_text.replace(
        cpp_title.split('_')[1].split('.')[0], 'hpp_title')
    hpp_text = hpp_text.replace('hpp_title',
                                cpp_title.split('_')[1].split('.')[0])
    # 判断是否已经存在文件，如果有就不改了
    if not os.path.exists(folder_path + '/include/' + cpp_title):
        send_message('{"text":"writing .hpp"}')
        with open(folder_path + '/include/' + cpp_title, 'w',
                  encoding='utf-8') as hpp_f:
            hpp_f.write(hpp_text)
    # 修改 main.cpp
    main_text = '#include"' + cpp_title + '"\n'
    with open(main_path, 'r', encoding='utf-8') as main_f:
        old_main_str = main_f.read()
        old_include_len = len(old_main_str.split('\n')[0])
        main_text += old_main_str[old_include_len + 1:]
    with open(main_path, 'w', encoding='utf-8') as main_f:
        main_f.write(main_text)
    send_message('{"text":"auto_movement_1.5"}')
    # os.startfile(main_path)# 打开clion（需要设置默认打开程序为clion）
    os.startfile(folder_path + '/launch_with_vscode.bat')
    send_message('{"text":"auto_movement_2"}')
    # 文档部分
    # 增加代码区域和题解区域
    note_name = title + '.md'
    note_name = note_name.replace(' ', '')
    if not os.path.exists(folder_path + '/notes/' + note_name):
        send_message('{"text":"writing .md"}')
        with open(folder_path + '/notes/' + note_name, 'w',
                  encoding='utf-8') as md_f:
            md_f.write('# ' + title + '\n')
            md_f.write(html2md(qContent))
            md_f.write("\n## 我的代码\n```c++\n```\n> \n\n## 题解\n```c++\n```\n")

    os.startfile(folder_path + '/notes/' + note_name)
    send_message('{"text":"auto_movement_3"}')
