from Tkinter import *
import os
import enrolment
import real_time_test
import warnings


def warn(msg, category):
    pass

warnings.warn = warn


def main():
    root = Tk()
    root.minsize(300, 200)
    win = Frame(root)
    win.pack()

    enrol = Button(win, text="Enrol", command=enrolment.begin_enrolment)
    enrol.pack(side=LEFT)

    rtt = Button(win, text="Real time test", command=real_time_test.test)
    rtt.pack(side=RIGHT)

    root.mainloop()


if __name__ == "__main__":
    main()
