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

        # ???????????? data????????? 0.1s????????????????????????
        if self.data == '' and self.process_times < self.max_process_times:
            time.sleep(0.1)
            self.process_messages()

    # ??????????????? data
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
        # ??????cmake_list??????????????????????????????????????????
        # ??????????????? m??????
        if title.find('?????????') != -1:
            send_message('{"text":"m"}')
            cpp_title = 'm'
            title_num_str = title.split('????????? ')[1]
            title_num_str = title_num_str.split('.')[0] + title_num_str.split(
                '.')[1]
        # ??? 0 ???????????? 5 ?????????
        for i in range(4 - len(title_num_str)):
            cpp_title += '0'
        cpp_title += title_num_str + '_'
        # .cpp????????????
        cpp_text = '#include"tools.hpp"\n\nusing namespace std;\n\n'
        cpp_text += codeText
        cpp_text += '\n\n// Start testing!\nint main() {\n    cout << "hello cmake!" << endl;\n    // Solution slt;\n    \n    return 0;\n}\n'

        # ??????????????????
        try:
            if codeText.find('Solution') != -1:  # ????????????
                eng_title = codeText.split('Solution')[1].split('(')[0].split(
                    ' ')[-1]
                # TODO: .cpp??????????????????????????????
            else:  # ???????????????
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
        send_message('{"text":"cpp_title:' + cpp_title + '"}')
        # ??????????????????????????????????????????????????????
        if not os.path.exists(src_path + '/' + cpp_title):
            send_message('{"text":"writing:' + cpp_title + '"}')
            with open(src_path + '/' + cpp_title, 'w',
                      encoding='utf-8') as cpp_f:
                cpp_f.write(cpp_text)
        #?????????bat???????????????????????????vscode????????????????????????
        with open(folder_path + '/launch_with_vscode.bat',
                  'w',
                  encoding='utf-8') as bat_f:
            bat_f.write("code " + folder_path + ' && ')
            bat_f.write("code " + src_path + '/' + cpp_title)

        # ?????? CMakeLists.txt
        with open(CML_path, 'w', encoding='utf-8') as cml_f:
            send_message('{"text":"writing:CMakeLists.txt"}')
            cml_f.write(
                '# cmake ?????????????????????\ncmake_minimum_required(VERSION 3.12)\n\n# ??????CMakeLists?????????????????????\nproject(cmakeTest)\n\n# ??????C++????????? C++ 11\nset(CMAKE_CXX_STANDARD 17)\n\n#?????????????????????,???????????????#include???.h?????????????????????\nINCLUDE_DIRECTORIES( ${PROJECT_SOURCE_DIR}/include)\n\n#????????????????????? ??????:add_executable(?????????????????? ????????????cpp)\nadd_executable(cmake_demo src/'
                + cpp_title + ' )')

        os.startfile(folder_path + '/launch_with_vscode.bat')  # bat??????vscode

        ## ????????????
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
                    "\n## ????????????\n\n```c++\n```\n> \n\n## ??????\n\n```c++\n```\n\n## ??????\n[0.?????????.md](0.?????????.md)\n["
                    + note_name + "](" + note_name + ")\n\n## ?????????\n")

        os.startfile(folder_path + '/notes/' + note_name)
        send_message('{"text":"auto_movement_3"}')


def Main():
    que = queue.Queue()
    # ?????????????????????
    hidden_process = HiddenProcess(que)
    # ??????????????????
    thread = threading.Thread(target=read_thread_func, args=(que, ))
    thread.daemon = True
    thread.start()
    # ??????????????????
    hidden_process.process_messages()
    # ????????????????????????????????????
    hidden_process.auto_movement()
    send_message('{"text":"bye"}')

    sys.exit(0)


if __name__ == '__main__':
    Main()
