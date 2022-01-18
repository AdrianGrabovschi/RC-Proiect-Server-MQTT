from server.ServerInstance import server
from interface.Notebook_Page import *
from interface.Interface_Utils import *
from tkinter.ttk import *
from tkinter import *
from Utils import printLog

class Server_Info(Notebook_Page):

    def __init__(self, notebook):
        Notebook_Page.__init__(self, notebook)

        Button(self.frame, text="Refresh", command=self.show_cients).place(x=WINDOW_WIDTH - 150, y=16+50, width=100)
        Button(self.frame, text="Disconect", command=self.disconnect_client).place(x=WINDOW_WIDTH - 150, y=16+100, width=100)

        self.dd_user = StringVar(self.frame)
        #self.dd_user.set(list(server.credentials.keys())[0])
        self.dd_user.set('all')

        users = ['all', *list(server.credentials.keys())]

        drop_down_menu = OptionMenu(self.frame, self.dd_user, *users, command=self.show_cients)
        drop_down_menu.place(x=WINDOW_WIDTH - 150, y=16, width=100)

        self.client_select_label = Label(self.frame, text='Selected client: ', fg='black')
        self.client_select_label.place(x=16, y=WINDOW_HEIGHT / 2, anchor=NW)

        self.to_be_disconnected = None

        self.tree = None
        self.client_tree = None
        self.show_cients()

    def show_cients(self, arg=''):
        columns = ['Client_ID', 'User', 'IP', 'PORT']

        if self.tree:
            self.tree.destroy()

        self.tree = Treeview(self.frame, columns=columns, show='headings', height=16)
        self.tree.place(x=16, y=16, anchor=NW)
        self.tree.bind('<ButtonRelease-1>', self.select_client)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, minwidth=0, width=(int)((WINDOW_WIDTH * 0.75) / len(columns)), stretch=NO)
        # self.tree.column(columns[0], width=0)

        for key, client in server.clients.items():
            if self.dd_user.get() == 'all' or client.userName == self.dd_user.get():
                self.tree.insert('', 'end', values=(client.clientID, client.userName, *client.addr))

    def select_client(self, arg):
        self.selected_client = self.tree.focus()

        if (self.selected_client is None):
            return

        client = self.tree.item(self.selected_client)['values']
        if len(client) == 0:
            return

        self.client_select_label['text'] = "Selected client: " + str(client)
        self.to_be_disconnected = client[0]

        columns = ['Topic', 'QoS']

        if self.client_tree:
            self.client_tree.destroy()

        self.client_tree = Treeview(self.frame, columns=columns, show='headings', height=8)
        self.client_tree.place(x=16, y=WINDOW_HEIGHT / 2 + 32, anchor=NW)
        # self.client_tree.bind('<ButtonRelease-1>', self.ceva)

        for column in columns:
            self.client_tree.heading(column, text=column)
            self.client_tree.column(column, minwidth=0, width=(int)((WINDOW_WIDTH * 0.75) / len(columns)), stretch=NO)
        # self.tree.column(columns[0], width=0)

        for topic in server.clients[client[0]].topics:
            self.client_tree.insert('', 'end', values=topic)

    def disconnect_client(self):
        #TODO disconnect handle
        printLog('DISCONNECT', self.to_be_disconnected)