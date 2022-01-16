from tkinter import *
from tkinter.ttk import Notebook

from Interface_Utils import *
from Server_Info_Page import Server_Info
from Topic_Info_Page import Topic_Info


class Interface:
    def __init__(self, server):
        self.server = server

        self.mainWindow = Tk()
        self.mainWindow.title('MQTT Server')
        self.mainWindow.geometry("%sx%s" %(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        notebook = Notebook(self.mainWindow)
        notebook.pack(fill='both', expand=True)

        serverInfoPage = Server_Info(notebook)
        topicInfoPage  = Topic_Info(notebook)

        serverInfoPage.frame.pack(fill='both', expand=True)
        topicInfoPage.frame.pack(fill='both', expand=True)

        notebook.add(serverInfoPage.frame,  text='Server Information')
        notebook.add(topicInfoPage.frame,   text='Topics Information')

    def create(self):
        self.server.start()
        self.mainWindow.mainloop()

    def on_closing(self):
        self.server.stop()
        self.mainWindow.destroy()



