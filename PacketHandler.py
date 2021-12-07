from enum import Enum
from Server import *
import struct

class Packet:
    def __init__(self, _conn, _addr, _packet_type, _data = None):
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
    printLog('DEBUG - len',  str_len)

    string = struct.unpack(str(str_len) + 's', data[offset + 2 : offset + 2 + str_len])[0]
    printLog('DEBUG - str', string)

    return offset + str_len + 2, string


def HandleCONNECT(server, packet):
    # primii doi bytes irelevanti

    (rlOffset, rlLen) = getPacketRemainingLength(packet)
    offset = rlOffset
    printLog('DEBUG - Offset', offset)

    offset, protocol_name = parsePacketString(packet.data, offset)

    protocol_level, conn_flags, keep_alive = struct.unpack('!BBH', packet.data[offset : offset + 4])
    offset += 4
    printLog('DEBUG - protocol_level', protocol_level)
    printLog('DEBUG - conn_flags', conn_flags)
    printLog('DEBUG - keep_alive', keep_alive)

    offset, client_id = parsePacketString(packet.data, offset)


