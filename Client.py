import time

class Client:
    def __init__(self, _clientID, _keepAliveInterval=60, _userName=None, _password=None):
        self.clientID = _clientID
        self.userName = _userName
        self.password = _password

        self.topics = []
        self.activeSession = True
        self.keepAliveInterval = _keepAliveInterval

        self.lastTimeActive = time.time()

