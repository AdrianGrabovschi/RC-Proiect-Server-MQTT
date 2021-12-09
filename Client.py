import time

class Client:
    def __init__(self, _conn, _addr, _clientID, _keepAliveInterval=60, _userName=None, _password=None):
        self.conn = _conn
        self.addr = _addr
        self.clientID = _clientID
        self.userName = _userName
        self.password = _password

        self.topics = []
        self.activeSession = True
        self.keepAliveInterval = _keepAliveInterval

        self.lastTimeActive = time.time()

