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
        self.running = False  # state-ul generic al serverului
        self.listenThread = None  # thread pentru ascultat conexiuni
        self.connectionThreads = []  # threaduri pentru conexiunile cu clientii
        self.clockThread = None  # thread pentru timer

        # server side stuff
        self.topics = {}  # {topic_name, coada de string-uri pentru ultimele 10 valori}
        self.topics_retain_msg = {} #{topic_name, topic_msg}
        self.clients = {}  # {client_id, Client}
        self.credentials = {}  # {user, pass}
        self.match_client_conn = {}  # {conn, client_id}

        self.timeout_clients = [] # array pentru gestionat timeout-ul clientilor pana la o a doua conectares

        self.read_users_and_passwords()
        self.read_topics()

        self.packet_id = 7777

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        printLog('INFO', 'Server starting on: ' + self.host + ':' + str(self.port))
        self.running = True

        # creaza si porneste thread-ul de listen
        self.listenThread = threading.Thread(target=self.listen)
        self.listenThread.start()

        # creaza si porneste thread-ul ceasului intern
        self.clockThread = Clock(1, self.tick)  # o data pe secunda tick()
        self.clockThread.start()

    def stop(self):
        self.running = False
        self.clockThread.running = False

        # opreste conextiunea cu toti clientii conectati
        for key, value in self.clients.items():
            value.conn.shutdown(socket.SHUT_RDWR)
            value.conn.close()

        # opreste socket ul de listen
        self.sock.close()

        # asteapta sa se inchida corect toate thread-urile de handle cu clientii
        for thread in self.connectionThreads:
            thread.join()

        # asteapta sa se inchida corecte thread-urile auxiliare
        self.clockThread.join()
        self.listenThread.join()
        printLog('INFO', 'Closing Server...', True)

    def tick(self):

        # actualizeaza black list-ul de timeout a clientilor
        self.timeout_clients = list(filter(lambda entry: not ((time.time() - entry[1]) > DISCONNECT_TIMEOUT), self.timeout_clients))

        # selecteaza clientii care trebuiesc deconectati in urma evaluarii sistemului de keep alive
        to_be_disconnected = []
        for client_id, client in self.clients.items():
            # printLog(client_id, time.time() - client.lastTimeActive)
            if (time.time() - client.lastTimeActive) > (client.keepAliveInterval * 1.5):
                to_be_disconnected.append(client_id)

        # deconecteaza clientii selectati
        for x in to_be_disconnected:
            self.disconnect_client(x)

    def disconnect_client(self, client_id):
        printLog('FORCE-DISCONNECT', client_id + ' ' + str(self.clients[client_id].addr))

        # adauga pe black list clientul pentru a evita reconectarea imediata
        self.timeout_clients.append((client_id, time.time()))

        # inchide socketul de comunicare cu respectivul client
        self.clients[client_id].conn.shutdown(socket.SHUT_RDWR)
        self.clients[client_id].conn.close()

        # sterge sesiunea curenta a clientului respectiv
        del self.match_client_conn[self.clients[client_id].addr]
        del self.clients[client_id]


    def listen(self):
        self.sock.listen()  # fara parametrii -> default, mai bine asa, sa si faca talentul cum stie el mai bine
        conn = None
        while self.running:
            try:
                (conn, addr) = self.sock.accept()   # asteapta conexiuni

                printLog('CONN', 'Server connected to ' + str(addr))

                # creaza si porneste thread pentru handle conexiune
                thread = threading.Thread(target=self.handleConnection, args=(conn, addr))
                self.connectionThreads.append(thread)
                thread.start()
            except:
                if conn:
                    conn.close()
                return

    def handleConnection(self, conn, addr):
        while self.running:
            try:
                data = conn.recv(1024)
            except:
                printLog('CONN', str(addr) + ' disconnected from server')
                return

            if not data:
                break

            printLog('RECV', 'Server recived ' + str(addr) + ': ' + str(data), True)

            # extrage tipul packetului din header
            packet_type = PACKET_TYPE(struct.unpack('B', data[0:1])[0] >> 4)
            printLog('Packet Type', str(addr) + ' -> ' + packet_type.name)

            # update lastTimeActive pentru KeepAlive
            if packet_type != PACKET_TYPE.CONNECT:
                client_id = self.match_client_conn[addr]
                self.clients[client_id].lastTimeActive = time.time()

            # handle efectiv al pachetului
            currentPacket = Packet(conn, addr, packet_type, data)

            # <3 update la client.lastTimeActive, cu un map de socket -> client ceva, vedem, detalii de implementare <3
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
                case PACKET_TYPE.PUBACK:
                    HandlePUBACK(self, currentPacket)
                case PACKET_TYPE.PUBREL:
                    HandlePUBREL(self, currentPacket)
                case PACKET_TYPE.PUBREC:
                    HandlePUBREC(self, currentPacket)
                case PACKET_TYPE.PUBCOMP:
                    HandlePUBCOMP(self, currentPacket)

                case _:  # default
                    printLog('ERROR', 'Invalid Packet: ' + packet_type.name)

        printLog('CONN', str(addr) + ' disconnected from server')
        conn.close()

    def sendPacket(self, packet):
        printLog('SEND-PACKET   -> ' + packet.packet_type.name, str(packet.addr) + ' -> ' + str(packet.data))
        try:
            packet.conn.sendall(packet.data)
        except:
            pass

    def read_users_and_passwords(self):
        file_path = CURRENT_PATH + '\\' + USERS_FILE_NAME
        file = open(file_path, "r")
        lines = file.read().splitlines()

        # decripteaza credentialele din fisier cu o cheie simetrica prestabilita
        for usr, pas in zip(*[iter(lines)] * 2):
            usr = cryptocode.decrypt(usr, "7804FCE44075FD6F8A014E31665B1E1E56BC16BE")
            pas = cryptocode.decrypt(pas, "7804FCE44075FD6F8A014E31665B1E1E56BC16BE")
            self.credentials[usr] = pas

        file.close()

    def read_topics(self):
        file_path = CURRENT_PATH + '\\' + TOPICS_FILE_NAME
        file = open(file_path, "r")
        lines = file.read().splitlines()

        for topic in lines:
            self.topics[topic] = deque()

        file.close()

    def nex_packet_id(self):  # genereaza un packet id nou si unic
        if (self.packet_id == (1 << 16)):
            self.packet_id = 7777  # hazul lui
        self.packet_id += 1
        return (self.packet_id)

    def dummy(self):
        print("dummmyymsdjkfghjksadf")
