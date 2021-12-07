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

            # packet_code = struct.unpack('B', data[0:1])[0] >> 4
            # printLog('Packet Code', str(addr) + ' -> ' + str(packet_code))
            packet_type = PACKET_TYPE(struct.unpack('B', data[0:1])[0] >> 4)
            printLog('Packet Type', str(addr) + ' -> ' + packet_type.name)

            currentPacket = Packet(conn, addr, packet_type, data)

            match packet_type:
                case PACKET_TYPE.CONNECT:
                    HandleCONNECT(self, currentPacket)
                case PACKET_TYPE.DISCONNECT:
                    HandleCONNECT(self, currentPacket)
                case _:  # default
                    printLog('ERROR', 'Invalid Packet: ' + packet_type.name)

        else:
            printLog('ERROR', str(addr) + ' -> Empty Packet')

    def sendPacket(self, packet):
        packet.conn.sendall(packet.data)

    def dummy(self):
        print("dummmyymsdjkfghjksadf")