#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 19:55
# @Author  : Eiya_ming
# @Email   : eiyaming@163.com
# @File    : old2.py
import queue
import struct
import sys
import threading
import time
import json
import re

# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
if sys.platform == "win32":
    import os
    import msvcrt

    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

# folder_path = 'E:/self_study/git/Google_LeetCode_extension/test_cmake'
folder_path = 'E:/self_study/git/cmake_demo'
# folder_path = 'E:\\self_study\\git\\cmake_demo'
src_path = folder_path + '/src'
CML_path = folder_path + '/CMakeLists.txt'
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
    s = s.replace('&gt', ">")

    return s


# Helper function that sends a message to the webapp.
def send_message(message):
    # Write message size.
    sys.stdout.buffer.write(struct.pack('I', len(message)))
    # Write the message itself.
    sys.stdout.write(message)
    sys.stdout.flush()


# Thread that reads messages from the webapp.
def read_thread_func(que):
    while 1:
        # Read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.buffer.read(4)
        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', text_length_bytes)[0]

        # Read the text (JSON object) of the message.
        byte_text = sys.stdin.buffer.read(text_length)
        # send_que.put('{"text":"byte got."}')
        # text = byte_text.decode(errors='ignore')
        text = byte_text.decode()
        que.put(text)


class HiddenProcess:
    def __init__(self, que):
        self.data = ''
        self.que = que
        self.connected = False
        self.process_times = 0
        self.max_process_times = 100
        self.data_dic = {}

    def process_messages(self):
        self.process_times += 1

        while not self.que.empty():
            message = self.que.get_nowait()
            if not self.connected:
                if message == '{"text":"c"}':
                    self.connected = True
                    send_message('{"text":"connected"}')
            else:
                if message.find('data') != -1:
                    send_message('{"text":"received"}')
                    self.data = message

        # 没有收到 data，延时 0.1s后，再运行本函数
        if self.data == '' and self.process_times < self.max_process_times:
            time.sleep(0.1)
            self.process_messages()

    # 自动化处理 data
    def auto_movement(self):
        send_message('{"text":"auto_movement"}')
        with open('test.json', 'w', encoding='utf-8') as f:
            f.write(self.data)
        with open('test.json', encoding='utf-8') as fp:
            self.data_dic = json.load(fp)
        send_message('{"text":"get data from json"}')
        title = self.data_dic['title'].encode('utf-8').decode('utf-8')
        qContent = self.data_dic['qContent'].encode('utf-8').decode('utf-8')
        codeText = self.data_dic['codeText'].encode('utf-8').decode('utf-8')
        send_message('{"text":"data to utf-8"}')

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
        # .cpp文件文本
        cpp_text = '#include"tools.hpp"\n\nusing namespace std;\n\n'
        cpp_text += codeText
        cpp_text += '\n\n// Start testing!\nint main() {\n    cout << "hello cmake!" << endl;\n    // Solution slt;\n    \n    return 0;\n}\n'

        # 提取英文名字
        try:
            if codeText.find('Solution') != -1:  # 正常题目
                eng_title = codeText.split('Solution')[1].split('(')[0].split(
                    ' ')[-1]
                # TODO: .cpp文件文本增加测试样例
            else:  # 设计类题目
                if codeText[0] != '/':
                    eng_title = codeText.split('class ')[1].split(' {')[0]
                else:
                    eng_title = codeText.split('\nclass ')[1].split(
                        ' {')[0][1].split(' {')[0]
            cpp_title += eng_title
            send_message('{"eng_title":"' + eng_title + '"}')
        except Exception:
            send_message('{"ERROR":"extract English name failed!"}')

        cpp_title += '.cpp'
        cpp_title = cpp_title.replace("*", "")  # 文件名不能加*
        send_message('{"text":"cpp_title:' + cpp_title + '"}')
        # 判断是否已经存在文件，如果有就不改了
        if not os.path.exists(src_path + '/' + cpp_title):
            send_message('{"text":"writing:' + cpp_title + '"}')
            with open(src_path + '/' + cpp_title, 'w',
                      encoding='utf-8') as cpp_f:
                cpp_f.write(cpp_text)
        #：修改bat文件，用于自动打开vscode并定位到编辑文件
        with open(folder_path + '/launch_with_vscode.bat',
                  'w',
                  encoding='utf-8') as bat_f:
            bat_f.write("code " + folder_path + ' && ')
            bat_f.write("code " + src_path + '/' + cpp_title)

        # 修改 CMakeLists.txt
        with open(CML_path, 'w', encoding='utf-8') as cml_f:
            send_message('{"text":"writing:CMakeLists.txt"}')
            cml_f.write(
                '# cmake 的最小版本要求\ncmake_minimum_required(VERSION 3.12)\n\n# 这个CMakeLists管理的工程名称\nproject(cmakeTest)\n\n# 设置C++标准为 C++ 11\nset(CMAKE_CXX_STANDARD 17)\n\n#设定头文件目录,主程序中的#include的.h文件坐在的目录\nINCLUDE_DIRECTORIES( ${PROJECT_SOURCE_DIR}/include)\n\n#生成可执行程序 语法:add_executable(可执行程序名 要编译的cpp)\nadd_executable(cmake_demo src/'
                + cpp_title + ' )')

        os.startfile(folder_path + '/launch_with_vscode.bat')  # bat打开vscode

        ## 文档部分
        note_name = title + '.md'
        note_name = note_name.replace(' ', '')
        if not os.path.exists(folder_path + '/notes/' + note_name):
            send_message('{"text":"writing .md"}')
            with open(folder_path + '/notes/' + note_name,
                      'w',
                      encoding='utf-8') as md_f:
                md_f.write('# ' + title + '\n')
                md_f.write(html2md(qContent))
                md_f.write(
                    "\n## 我的代码\n\n```c++\n" + codeText +
                    "\n```\n> \n\n## 题解\n\n```c++\n```\n\n## 标签\n[0.典型题.md](0.典型题.md)\n["
                    + note_name + "](" + note_name + ")\n\n## 知识点\n")

        os.startfile(folder_path + '/notes/' + note_name)
        send_message('{"text":"auto_movement_3"}')


def Main():
    que = queue.Queue()
    # 处理对象初始化
    hidden_process = HiddenProcess(que)
    # 接收线程开启
    thread = threading.Thread(target=read_thread_func, args=(que, ))
    thread.daemon = True
    thread.start()
    # 处理接收信息
    hidden_process.process_messages()
    # 自动化创建文件，打开软件
    hidden_process.auto_movement()
    send_message('{"text":"bye"}')

    sys.exit(0)


if __name__ == '__main__':
    Main()
