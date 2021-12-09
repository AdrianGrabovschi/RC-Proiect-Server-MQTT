import sys

from Server import *
#from App import *
SERVER_HOST = 'localhost'
SERVER_PORT = 7777

if __name__ == "__main__":
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()
    # app = QApplication(sys.argv)
    # windows = App()
    # sys.exit(app.exec_())