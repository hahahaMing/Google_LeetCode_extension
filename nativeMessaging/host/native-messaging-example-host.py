#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# A simple native messaging host. Shows a tkinter dialog with incoming messages
# that also allows to send message back to the webapp.

import queue
import struct
import sys
import threading

try:
    import tkinter
    from tkinter import messagebox
except ImportError:
    tkinter = None

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

    message_number = 0
    while 1:
        # Read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.buffer.read(4)
        if len(text_length_bytes) == 0:
            if que:
                que.put(None)
            sys.exit(0)

        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', text_length_bytes)[0]

        # Read the text (JSON object) of the message.
        # text = sys.stdin.read(text_length).decode('utf-8')
        text = sys.stdin.read(text_length)
        if que:
            que.put(text)
        else:
            # In headless mode just send an echo message back.
            send_message('{"echo": %s}' % text)


if tkinter:
    class NativeMessagingWindow(tkinter.Frame):
        def __init__(self, que):
            self.que = que

            tkinter.Frame.__init__(self)
            self.pack()

            self.text = tkinter.Text(self)
            self.text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
            self.text.config(state=tkinter.DISABLED, height=10, width=40)

            self.messageContent = tkinter.StringVar()
            self.sendEntry = tkinter.Entry(self, textvariable=self.messageContent)
            self.sendEntry.grid(row=1, column=0, padx=10, pady=10)

            self.sendButton = tkinter.Button(self, text="Send", command=self.onSend)
            self.sendButton.grid(row=1, column=1, padx=10, pady=10)

            self.after(100, self.processMessages)

        def processMessages(self):
            while not self.que.empty():
                message = self.que.get_nowait()
                if message is None:
                    self.quit()
                    return
                self.log("Received %s" % message)
                # 添加功能：
                # 接收到"txt"就创建一个名为test.txt的txt文件
                if message == '{"text":"txt"}':
                    with open("test.txt",'w',encoding='utf-8')as f:
                        f.write("test ok!\n")
                        self.log("test creating file ok!")
                
                if message == '{"text":"edit"}':
                    with open("test.txt",'a',encoding='utf-8')as f:
                        f.write("edit ok!\n")
                        self.log("test editing file ok!")

                if message == '{"text":"open"}':
                    # os.startfile(r'E:\Program Files\JetBrains\CLion 2019.3.5\bin\clion64.exe')

                    os.startfile(r'C:\Users\15518\Desktop\test.md')
                    self.log("opening Typora ok!")

            self.after(100, self.processMessages)

        def onSend(self):
            text = '{"text": "' + self.messageContent.get() + '"}'
            self.log('Sending %s' % text)
            try:
                send_message(text)

            except IOError:
                messagebox.showinfo('Native Messaging Example',
                                    'Failed to send message.')
                sys.exit(1)

        def log(self, message):
            self.text.config(state=tkinter.NORMAL)
            self.text.insert(tkinter.END, message + "\n")
            self.text.config(state=tkinter.DISABLED)


def Main():
    if not tkinter:
        send_message('"tkinter python module wasn\'t found. Running in headless ' +
                     'mode. Please consider installing tkinter."')
        read_thread_func(None)
        sys.exit(0)

    que = queue.Queue()

    main_window = NativeMessagingWindow(que)
    main_window.master.title('Native Messaging Example')

    thread = threading.Thread(target=read_thread_func, args=(que,))
    thread.daemon = True
    thread.start()

    main_window.mainloop()


    sys.exit(0)


if __name__ == '__main__':
    Main()