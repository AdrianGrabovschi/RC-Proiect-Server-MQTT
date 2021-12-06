import socket
import struct
import threading

from Utils import *
from PacketHandler import *

class Server:
    def __init__(self, _HOST, _PORT):
        # network stuff
        self.host = _HOST
        self.port = _PORT
        self.sock = None

        # configs
        self.running = False # state-ul generic al serverului

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        printLog('info', 'Server starting on: ' + self.host + ':' + str(self.port))
        self.running = True

        self.listen()

    def listen(self):
        self.sock.listen() # fara parametrii -> default, mai bine asa, sa si faca talentul cum stie el mai bine
        while self.running:
            (conn, addr) = self.sock.accept()
            printLog('conn', 'Server connected to ' + str(addr))
            threading.Thread(target=self.handlePacket, args=(conn, addr)).start()

    def handlePacket(self, conn, addr):
        data = conn.recv(1024)
        if data:
            printLog('recv', 'Server recived ' + str(addr) + ': ' + str(data))

            packet_type = PACKET_TYPE(struct.unpack('!H', data[0:2])[0])
            printLog('Packet Type', str(addr) + ' -> ' + packet_type.name)

            currentPacket = Packet(conn, addr, packet_type, data)

            match packet_type:
                case PACKET_TYPE.CONNECT:
                    HandleCONNECT(self, currentPacket)
                case PACKET_TYPE.CONNACK:
                    return False
                case _:  # default
                    printLog('ERROR', 'Invalid Packet: ' + packet_type.name)

        else:
            printLog('ERROR', str(addr) + ' -> Empty Packet')

    def dummy(self):
        print("dummmyymsdjkfghjksadf")