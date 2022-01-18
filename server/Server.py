import struct
import cryptocode
from Utils import *
from server.PacketHandler import *
from collections import deque
import socket


class Server:
    def __init__(self, _HOST, _PORT):
        # network stuff
        self.host = _HOST
        self.port = _PORT
        self.sock = None

        # configs
        self.running = False        # state-ul generic al serverului
        self.listenThread = None    # thread pentru ascultat conexiuni
        self.clockThread = None     # thread pentru timer

        # server side stuff
        self.topics = {}            # {topic_name, coada de string-uri pentru ultimele 10 valori}
        self.clients = {}           # {client_id, Client}
        self.credentials = {}       # {user, pass}
        self.match_client_conn = {} # {conn, client_id}

        self.read_users_and_passwords()
        self.read_topics()

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        printLog('INFO', 'Server starting on: ' + self.host + ':' + str(self.port))
        self.running = True

        self.listenThread = threading.Thread(target=self.listen)
        self.listenThread.start()

        self.clockThread = Clock(1, self.tick)  # o data pe secunda tick()
        self.clockThread.start()

    def stop(self):
        self.running = False
        self.clockThread.running = False

        for key, value in self.clients.items():
            value.conn.close()

        self.sock.close()
        self.clockThread.join()
        self.listenThread.join()
        printLog('INFO', 'Closing Server...', True)

    def tick(self):
        pass
        """
        for clientID in self.clients:
            printLog('CLOCK', str(clientID) + ':' + str(self.clients[clientID].userName) +
                     ' -> activ de: ' + str(round(time.time()-self.clients[clientID].lastTimeActive)) + ' secunde')
        """

    def listen(self):
        self.sock.listen()  # fara parametrii -> default, mai bine asa, sa si faca talentul cum stie el mai bine
        conn = None
        while self.running:
            try:
                (conn, addr) = self.sock.accept()
                printLog('CONN', 'Server connected to ' + str(addr))
                threading.Thread(target=self.handleConnection, args=(conn, addr)).start()
            except:
                if conn:
                    conn.close()
                pass

    def handleConnection(self, conn, addr):
        while self.running:
            try:
                data = conn.recv(1024)
            except:
                pass

            if not data:
                break

            printLog('RECV', 'Server recived ' + str(addr) + ': ' + str(data), True)

            # packet_code = struct.unpack('B', data[0:1])[0] >> 4
            # printLog('Packet Code', str(addr) + ' -> ' + str(packet_code))
            packet_type = PACKET_TYPE(struct.unpack('B', data[0:1])[0] >> 4)
            printLog('Packet Type', str(addr) + ' -> ' + packet_type.name)

            currentPacket = Packet(conn, addr, packet_type, data)

            # update la client.lastTimeActive, cu un map de socket -> client ceva, vedem, detalii de implementare
            match packet_type:
                case PACKET_TYPE.CONNECT:
                    HandleCONNECT(self, currentPacket)
                case PACKET_TYPE.PUBLISH:
                    HandlePUBLISH(self, currentPacket)
                case PACKET_TYPE.PINGREQ:
                    HandlePINGREQ(self, currentPacket)
                case PACKET_TYPE.DISCONNECT:
                    HandleDISCONNECT(self, currentPacket)
                case PACKET_TYPE.SUBSCRIBE:
                    HandleSUBSCRIBE(self, currentPacket)
                case _:  # default
                    printLog('ERROR', 'Invalid Packet: ' + packet_type.name)

        printLog('CONN', str(addr) + ' disconnected from server')
        conn.close()

    def sendPacket(self, packet):
        printLog('SEND', str(packet.addr) + ' -> ' + str(packet.data))
        try:
            packet.conn.sendall(packet.data)
        except:
            pass
    def read_users_and_passwords(self):
        file_path = CURRENT_PATH + '\\' + USERS_FILE_NAME
        file = open(file_path, "r")
        lines = file.read().splitlines()

        for usr, pas in zip(*[iter(lines)]*2):
            usr = cryptocode.decrypt(usr, "7804FCE44075FD6F8A014E31665B1E1E56BC16BE")
            pas = cryptocode.decrypt(pas, "7804FCE44075FD6F8A014E31665B1E1E56BC16BE")
            self.credentials[usr] = pas

        file.close()

    def read_topics(self):
        file_path = CURRENT_PATH + '\\' + TOPICS_FILE_NAME
        file = open(file_path, "r")
        lines = file.read().splitlines()

        for topic in lines:
            self.topics[topic] = deque(("aaaaa", "bbbbb", "ccccc"))

        file.close()


    def dummy(self):
        print("dummmyymsdjkfghjksadf")
