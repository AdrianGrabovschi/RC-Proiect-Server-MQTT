from __future__ import print_function

import os
import threading
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 7777

CURRENT_PATH = os.getcwd()
USERS_FILE_NAME = 'secret.txt'

class Clock(threading.Thread):
    def __init__(self, interval, tick):
        self.running = True
        self.start_timestamp = time.time() # in caz ca trebuie
        self.target_function = tick
        self.interval = interval
        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            self.target_function()
            time.sleep(self.interval)


def printLog(msg_type, msg='', newLine=False):
    if newLine:
        print('')
    print("[" + msg_type.upper() + "]\t" + str(msg))
