from tkinter import *
from tkinter.messagebox import showinfo
from dbconnect import *

def comiclist(config):
    database = DB(config)

Label(text='Next Comic').pack()
mainloop()
