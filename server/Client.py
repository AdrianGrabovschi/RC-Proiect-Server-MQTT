import time

class Client:
    def __init__(self, _conn, _addr, _clientID, _keepAliveInterval=60, _userName=None):
        self.conn = _conn           # connexiunea cu clientul
        self.addr = _addr           # adresa clientului
        self.clientID = _clientID   # id-ul unic al clientului
        self.userName = _userName   # username-ul sub care s-a conectat

        self.topics = []            # topicurile la care s-a abonat
        self.activeSession = True   # flagul de sesiune activa
        self.keepAliveInterval = _keepAliveInterval # intervalul pentru keep alive dat la conectare

        self.lastTimeActive = time.time()           # timestamp-ul ultimei interactiuni cu serverul

