from __future__ import print_function
import sys
import threading
import time
import datetime
#clasa timer in threading

class Clock(threading.Thread):
    def __init__(self, interval, tick):
        self.start_timestamp = time.time() # in caz ca trebuie
        self.target_function = tick
        self.interval = interval
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.target_function()
            time.sleep(self.interval)


def printLog(msg_type, msg):
    print("[" + msg_type.upper() + "]\t" + str(msg))
