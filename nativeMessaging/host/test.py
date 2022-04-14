import queue
import struct
import sys
import threading
import time
import json
import re
import logging


# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
# if sys.platform == "win32":
import os
import msvcrt

msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


# Helper function that sends a message to the webapp.
def send_message(message):
    logging.info("sending: " + message)
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
        logging.info("read: "+text)


class HiddenProcess:
    def __init__(self, que):
        self.data = ''

    def process_messages(self):
        pass

    # 自动化处理 data
    def auto_movement(self):
        pass


def Main():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
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
    logging.info("bye.")
    sys.exit(0)


if __name__ == '__main__':
    Main()
