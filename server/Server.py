from server.PacketHandler import *
import socket

class Server:
    def __init__(self, _HOST, _PORT):
        # network stuff
        self.host = _HOST
        self.port = _PORT
        self.sock = None

        # configs
        self.running = False # state-ul generic al serverului
        self.listenThread = None
        self.clockThread = None

        # server side stuff
        self.clients = {}


    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        printLog('info', 'Server starting on: ' + self.host + ':' + str(self.port))
        self.running = True

        self.listenThread = threading.Thread(target=self.listen)
        self.listenThread.start()

        self.clockThread = Clock(1, self.tick) # o data pe secunda tick()
        self.clockThread.start()

    def stop(self):
        self.running = False
        self.sock.close()

    def tick(self):
        for clientID in self.clients:
            printLog('CLOCK', str(clientID) + ':' + str(self.clients[clientID].userName) + ' -> activ de:' + str(time.time()-self.clients[clientID].lastTimeActive))

    def listen(self):
        self.sock.listen() # fara parametrii -> default, mai bine asa, sa si faca talentul cum stie el mai bine
        while self.running:
            (conn, addr) = self.sock.accept()
            printLog('CONN', 'Server connected to ' + str(addr))
            threading.Thread(target=self.handleConnection, args=(conn, addr)).start()

    def handleConnection(self, conn, addr):
        while self.running:
            data = conn.recv(1024)
            if not data:
                break
            printLog('RECV', 'Server recived ' + str(addr) + ': ' + str(data))

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
                case _:  # default
                    printLog('ERROR', 'Invalid Packet: ' + packet_type.name)

        printLog('INFO', str(addr) + ' disconnected from server')
        conn.close()

    def sendPacket(self, packet):
        printLog('SEND', str(packet.addr) + ' -> ' + str(packet.data))
        packet.conn.sendall(packet.data)

    def dummy(self):
        print("dummmyymsdjkfghjksadf")