from tkinter import E, SUNKEN, W, Frame, Label


class LogFrame(Frame):
    def __init__(self, parent=None, meret=0):
        Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=meret)
        self.status = Label(self, text='', anchor=W, relief=SUNKEN, bd=1, width=20)
        self.status.grid(row=0, column=0, sticky=W + E)

    def log(self, string):
        self.status.config(text=string)
