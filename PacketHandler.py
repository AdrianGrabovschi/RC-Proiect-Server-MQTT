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

def HandleCONNECT(server, packet):
    # primii doi bytes irelevanti

    (rlOffset, rlLen) = getPacketRemainingLength(packet)
    Offset = rlOffset
    printLog('DEBUG - Offset', Offset)

    protocol_name_len = struct.unpack('!H', packet.data[Offset : Offset + 2])[0]
    Offset += 2
    printLog('DEBUG - protocol_name_len', protocol_name_len)

    protocol_name = struct.unpack(str(protocol_name_len) + 's', packet.data[Offset : Offset + protocol_name_len])[0]
    Offset += protocol_name_len
    printLog('DEBUG - protocol_name', protocol_name)

    protocol_level, conn_flags, keep_alive = struct.unpack('!BBH', packet.data[Offset : Offset + 4])
    Offset += 4
    printLog('DEBUG - protocol_level', protocol_level)
    printLog('DEBUG - conn_flags', conn_flags)
    printLog('DEBUG - keep_alive', keep_alive)

    client_id_len = struct.unpack('!H', packet.data[Offset : Offset + 2])[0]
    Offset += 2
    printLog('DEBUG - client_id_len', client_id_len)

    client_id = struct.unpack(str(client_id_len) + 's', packet.data[Offset : Offset + client_id_len])[0]
    Offset += client_id_len
    printLog('DEBUG - client_id', client_id)

    # bla bla gestiune client