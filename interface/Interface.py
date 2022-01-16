from Window import *

class Interface:
    def __init__(self):
        self.window = Tk()
        self.mywin = Window(self.window)
        self.window.title('MQTT Server')
        self.window.geometry("512x512")

    def create(self):
        self.window.mainloop()

