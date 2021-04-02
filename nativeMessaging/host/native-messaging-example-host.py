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
                if message.find('data'):
                    send_message('{"text":"received"}')
                    self.data = message

        # 没有收到 data，延时 0.1s后，再运行本函数
        if self.data == '' and self.process_times < self.max_process_times:
            time.sleep(0.1)
            self.process_messages()

    # 自动化处理 data
    def auto_movement(self):
        send_message('{"text":"auto_movement"}')
        with open('test.json', 'w', encoding='utf-8')as f:
            f.write(self.data)
        with open('test.json', encoding='utf-8')as fp:
            self.data_dic = json.load(fp)
        title = self.data_dic['title'].encode('utf-8').decode('utf-8')
        qContent = self.data_dic['qContent'].encode('utf-8').decode('utf-8')
        codeText = self.data_dic['codeText'].encode('utf-8').decode('utf-8')
        # 搞定。。。
        codeText = codeText.replace('\xa0', ' ')
        eng_title = ''
        hpp_title = 'q'
        title_num_str = title.split('.')[0]
        if title.find('面试题') != -1:
            send_message('{"text":"m"}')
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
            send_message('{"text":"writing .hpp"}')
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
        # todo: 增加代码区域和题解区域
        note_name = hpp_title.split('.')[0] + '.md'
        if not os.path.exists(folder_path + '/notes/' + note_name):
            send_message('{"text":"writing .md"}')
            with open(folder_path + '/notes/' + note_name, 'w', encoding='utf-8')as md_f:
                md_f.write('# ' + title + '\n')
                md_f.write(html2md(qContent))
                md_f.write("\n## 我的代码\n```c++\n```\n> \n\n## 题解\n")
        os.startfile(folder_path + '/notes/' + note_name)


def Main():
    que = queue.Queue()
    # 处理对象初始化
    hidden_process = HiddenProcess(que)
    # 接收线程开启
    thread = threading.Thread(target=read_thread_func, args=(que,))
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
