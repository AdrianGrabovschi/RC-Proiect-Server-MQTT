import os

LOG_FILE_NAME = 'server.log'

if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)

log_file = open(LOG_FILE_NAME, 'w')
