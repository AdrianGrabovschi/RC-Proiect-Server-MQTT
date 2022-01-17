from server.ServerInstance import server
from interface.Notebook_Page import *
from interface.Interface_Utils import *
from tkinter.ttk import *
from tkinter import *

class Topic_Info(Notebook_Page):

    def __init__(self, notebook):
        Notebook_Page.__init__(self, notebook)

        Button(self.frame, text="Refresh", command=self.show_topics).place(x=WINDOW_WIDTH - 150, y=50, width=100)

        self.dd_topic = StringVar(self.frame)
        self.dd_topic.set(list(server.topics.keys())[0])

        drop_down_menu = OptionMenu(self.frame, self.dd_topic, *list(server.topics.keys()), command=self.show_topics)
        drop_down_menu.place(x=WINDOW_WIDTH - 150, y=16, width=100)

        self.tree = None
        self.show_topics()

    def show_topics(self, arg=''):
        columns = ['Message']

        if self.tree:
            self.tree.destroy()

        self.tree = Treeview(self.frame, columns=columns, show='headings', height=16)
        self.tree.place(x=16, y=16, anchor=NW)
        self.tree.bind('<ButtonRelease-1>', self.dummy)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, minwidth=0, width=(int)((WINDOW_WIDTH * 0.75) / len(columns)), stretch=NO)
        # self.tree.column(columns[0], width=0)

        topic = server.topics['topic1']
        if len(topic) != 0:
            for msg in topic:
                self.tree.insert('', 'end', values=msg)


    def dummy(self):
        print("server_info_dummy")
        pass