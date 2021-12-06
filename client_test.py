import socket
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 7777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST,SERVER_PORT))
data = struct.pack("!H", 1)
sock.send(data)
print (sock.recv(1024))