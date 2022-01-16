from Notebook_Page import *
from Interface_Utils import *
from tkinter.ttk import *
from tkinter import *

class Server_Info(Notebook_Page):

    def __init__(self, notebook):
        Notebook_Page.__init__(self, notebook)

        Button(self.frame, text="Modify", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=50)

        Button(self.frame, text="Insert", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=90)

        Button(self.frame, text="Delete", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=130)

        self.show_cients()

    def show_cients(self):
        self.tree = Treeview(self.frame, columns=['aaaaa', 'bbbb'], show='headings', height=13)
        self.tree.place(x=16, y=16, anchor=NW)
        self.tree.bind('<ButtonRelease-1>', self.dummy)

        """
        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, minwidth=0, width=(int)(WINDOW_WIDTH / len(columns)) - 8, stretch=NO)
        # self.tree.column(columns[0], width=0)
        """



        #self.tree.insert('', 'end', values=results)

    def dummy(self):
        pass