from Server import *

SERVER_HOST = 'localhost'
SERVER_PORT = 7777

if __name__ == "__main__":
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()
