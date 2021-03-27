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

# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
if sys.platform == "win32":
    import os
    import msvcrt

    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


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
        # send_message('{"text":"write done"}')
        with open('test.json', encoding='utf-8')as fp:
            self.data_dic = json.load(fp)
        title = self.data_dic['title']
        qContent = self.data_dic['qContent']
        codeText = self.data_dic['codeText']
        # todo: 1.



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
