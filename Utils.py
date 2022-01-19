import os
import threading
import time

MAX_LAST_TOPIC_ENTRIES = 10
DISCONNECT_TIMEOUT = 10

CURRENT_PATH = os.getcwd()
USERS_FILE_NAME = 'secret.txt'
TOPICS_FILE_NAME = 'topics.txt'
LOG_FILE_NAME = 'server.log'

if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)

log_file = open(LOG_FILE_NAME, 'w')

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
        log_file.write('\n')
    print("[" + msg_type.upper() + "]\t" + str(msg))
    log_file.write("[" + msg_type.upper() + "]\t" + str(msg) + "\n")