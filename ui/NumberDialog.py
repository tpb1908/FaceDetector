from ui.Dialog import Dialog
from Tkinter import *


class NumberDialog(Dialog):

    def __init__(self, parent, callback, title="Input percentage"):
        Dialog.__init__(self, parent, callback, title)
        # super(NumberDialog, self).__init__(parent, title)

    def body(self, master):
        Label(master, text="Input").grid(row=0)

        self.input = Entry(master)

        self.input.grid(row=0, column=1)

        return self.input

    def apply(self):
        try:
            return int(self.input.get())
        except ValueError:
            return 50
