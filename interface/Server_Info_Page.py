import time
from server.ServerInstance import server
from interface.Notebook_Page import *
from interface.Interface_Utils import *
from tkinter.ttk import *
from tkinter import *

class Server_Info(Notebook_Page):

    def __init__(self, notebook):
        Notebook_Page.__init__(self, notebook)

        Button(self.frame, text="Modify", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=50)

        Button(self.frame, text="Insert", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=90)

        Button(self.frame, text="Delete", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=130)

        self.tree = None
        self.show_cients()

    def show_cients(self):
        columns = ['User', 'Client_ID']

        if self.tree:
            self.tree.destroy()

        self.tree = Treeview(self.frame, columns=columns, show='headings', height=16)
        self.tree.place(x=16, y=16, anchor=NW)
        self.tree.bind('<ButtonRelease-1>', self.dummy)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, minwidth=0, width=(int)((WINDOW_WIDTH / 2) / len(columns)), stretch=NO)
        # self.tree.column(columns[0], width=0)

        for key, values in server.clients.items():
            self.tree.insert('', 'end', values=(values.userName, values.clientID))

        #self.tree.insert('', 'end', values=results)

    def dummy(self):
        self.show_cients()
        print("server_info_dummy")
        for key, value in server.clients.items():
            print((key, value))
        pass