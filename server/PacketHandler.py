import struct
from enum import Enum
from Utils import *
from server.Server import *
from server.Client import *

class Packet:
    def __init__(self, _conn, _addr, _packet_type, _data=None):
        self.conn = _conn
        self.addr = _addr
        self.data = _data
        self.packet_type = _packet_type

class PACKET_TYPE(Enum):
    RESERVED    = 0
    CONNECT     = 1
    CONNACK     = 2
    PUBLISH     = 3
    PUBACK      = 4
    PUBREC      = 5
    PUBREL      = 6
    PUBCOMP     = 7
    SUBSCRIBE   = 8
    SUBACK      = 9
    UNSUBSCRIBE = 10
    UNSUBACK    = 11
    PINGREQ     = 12
    PINGRESP    = 13
    DISCONNECT  = 14
    Reserved    = 15

class CONNECTION_FLAGS(Enum):
    CLEAN_SESSION = (1 << 1)
    WILL_FLAG     = (1 << 2)
    WILL_QOS1     = (1 << 3)
    WILL_QOS2     = (1 << 4)
    WILL_RETAIN   = (1 << 5)
    PASSWORD      = (1 << 6)
    USER_NAME     = (1 << 7)

class CONNACK_RETURN_CODES(Enum):
    ACCEPTED                        = 0
    UNACCEPTABLE_PROTOCOL_VERSION   = 1
    IDENTIFIER_REJECTED             = 2
    SERVER_UNAVAILABLE              = 3
    BAD_CREDENTIALS                 = 4
    NOT_AUTHORIZED                  = 5


# cc: https://docs.solace.com/MQTT-311-Prtl-Conformance-Spec/MQTT%20Control%20Packet%20format.htm#_Ref355703004
def getPacketRemainingLength(packet):
    multiplier = 1
    value = 0
    index = 1
    while True:
        byte = packet.data[index]
        value += (byte & 127) * multiplier
        if not(byte & 128):
            break
        multiplier = multiplier * 128
        index += 1
    return index + 1, value

def parsePacketString(data, offset):
    str_len = struct.unpack('!H', data[offset : offset + 2])[0]
    #printLog('parse-Packet-String - len',  str_len)

    string = struct.unpack(str(str_len) + 's', data[offset + 2 : offset + 2 + str_len])[0]
    #printLog('parse-Packet-String - str', string)

    return offset + str_len + 2, string

def generateCONNACKPacket(conn, addr, sp_bit, returnCode):
    packet = Packet(conn, addr, PACKET_TYPE.CONNACK)
    packet.data = struct.pack('BBBB', PACKET_TYPE.CONNACK.value << 4, 2, sp_bit, returnCode)
    #                                           ^1                    ^2 ^3      ^4
    # 1 -> packet type
    # 2 -> variable header length
    # 3 -> Connect Acknowledge Flags x00 mereu din fericire
    # 4 -> code return-ul CONNACK-ului
    return packet

def generatePINGRESPPacket(conn, addr):
    packet = Packet(conn, addr, PACKET_TYPE.PINGRESP)
    packet.data = struct.pack('BB',  PACKET_TYPE.PINGRESP.value << 4, 0)

    return packet

def HandleCONNECT(server, packet):
    printLog('NEW-PACKET -> CONNECT', '--------------------------------------------------------------')

    # primii doi bytes irelevanti
    (rlOffset, rlLen) = getPacketRemainingLength(packet)
    offset = rlOffset

    offset, protocol_name = parsePacketString(packet.data, offset)

    protocol_level, conn_flags, keep_alive = struct.unpack('!BBH', packet.data[offset : offset + 4])
    offset += 4

    offset, client_id = parsePacketString(packet.data, offset)
    client_id = client_id.decode('ascii')

    if conn_flags & CONNECTION_FLAGS.CLEAN_SESSION.value:
        #printLog("CONN_FLAG", 'YUHUHUI, are FLAG de CLEAN_SESSION')
        sp_connack_bit = 0
    else:
        #implementare pentru clean session 0(daca serverul a stocat sesiunea, sp_connack_bit = 1, altfel 0)
        pass

    if conn_flags & CONNECTION_FLAGS.WILL_FLAG.value:
        #printLog("CONN_FLAG", 'YUHUHUI, are FLAG de WILL_FLAG')
        pass

    will_qos = ((conn_flags & CONNECTION_FLAGS.WILL_QOS2.value) >> 4) | ((conn_flags & CONNECTION_FLAGS.WILL_QOS1.value) >> 2)
    #printLog("CONN_FLAG", 'YUHUHUI, are FLAG de WILL_QOS: ' + str(will_qos))

    if conn_flags & CONNECTION_FLAGS.WILL_RETAIN.value:
        #printLog("CONN_FLAG", 'YUHUHUI, are FLAG de WILL_RETAIN')
        pass

    if conn_flags & CONNECTION_FLAGS.PASSWORD.value:
        #printLog("CONN_FLAG", 'YUHUHUI, are FLAG de PASSWORD')
        pass

    if conn_flags & CONNECTION_FLAGS.USER_NAME.value:
        #printLog("CONN_FLAG", 'YUHUHUI, are FLAG de USER_NAME')
        pass

    # WILL_TOPIC
    will_topic = ''
    will_message = ''
    if conn_flags & CONNECTION_FLAGS.WILL_FLAG.value:
        offset, will_topic = parsePacketString(packet.data, offset)
        #printLog("will_topic", will_topic)

        offset, will_message = parsePacketString(packet.data, offset)
        #printLog("will_message", will_message)

    user_name = ''
    if conn_flags & CONNECTION_FLAGS.USER_NAME.value:
        offset, user_name = parsePacketString(packet.data, offset)
        user_name = user_name.decode('ascii')
        #printLog("user_name", user_name)

    password = ''
    if conn_flags & CONNECTION_FLAGS.PASSWORD.value:
        offset, password = parsePacketString(packet.data, offset)
        password = password.decode('ascii')
        #printLog("password: ", password)

    #TODO aici vin checkuri pentru corectitudinea datelor, ne apucam de connack si vedem dupa care e mersul aici
    return_code = CONNACK_RETURN_CODES.ACCEPTED.value
    if protocol_level != 4:
        return_code = CONNACK_RETURN_CODES.UNACCEPTABLE_PROTOCOL_VERSION.value

    if not ((user_name in server.credentials) and (server.credentials[user_name] == password)):
        return_code = CONNACK_RETURN_CODES.BAD_CREDENTIALS.value

    if client_id in server.clients:
        return_code = CONNACK_RETURN_CODES.IDENTIFIER_REJECTED.value

    # daca e totu ca la abecedar trimitem connack-ul
    to_send_packet = generateCONNACKPacket(packet.conn, packet.addr, sp_connack_bit, return_code) # 0 -> ACCEPTED
    server.sendPacket(to_send_packet)

    if return_code == CONNACK_RETURN_CODES.ACCEPTED.value:
        new_client = Client(packet.conn, packet.addr, client_id, keep_alive, user_name)
        server.clients[client_id] = new_client
        server.match_client_conn[packet.addr] = client_id

    #printLog('END-PACKET -> CONNECT', '--------------------------------------------------------------')

def HandlePUBLISH(server, packet):
    printLog('NEW-PACKET -> PUBLISH', '--------------------------------------------------------------')


def HandlePINGREQ(server, packet):
    printLog('NEW-PACKET -> PINGREQ', '--------------------------------------------------------------')
    to_send_packet = generatePINGRESPPacket(packet.conn, packet.addr)

    server.sendPacket(to_send_packet)


def HandleDISCONNECT(server, packet):
    printLog('NEW-PACKET -> DISCONNECT', '--------------------------------------------------------------')
    printLog('DISCONNECT', 'say byebye to ' + str(packet.addr))
    client_id = server.match_client_conn[packet.addr]
    del server.clients[client_id]
    del server.match_client_conn[packet.addr]

   # print(server.clients)

