import socket
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 7777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST,SERVER_PORT))
data = struct.pack("!B", 1)

#sock.send(b'\x10\x10\x00\x06MQQQTT\x04\x02\x00\x3C\x00\x08DIGIDIGI')
sock.send(b'\x10\x10\x00\x06MQQQTT\x04\xFF\x00\x3C\x00\x08DIGIDIGI\x00\x03AAA\x00\x03BBB\x00\x03CCC\x00\x03DDD')

print (sock.recv(1024))