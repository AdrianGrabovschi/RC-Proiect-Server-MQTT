from Notebook_Page import *
from Interface_Utils import *
from tkinter import *

class Topic_Info(Notebook_Page):

    def __init__(self, notebook):
        Notebook_Page.__init__(self, notebook)

        Button(self.frame, text="asdasdasd", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=50)

        Button(self.frame, text="asdasdasd", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=90)

        Button(self.frame, text="asdasdasd", command=self.dummy).place(x=WINDOW_WIDTH - 150, y=130)

    def dummy(self):
        pass