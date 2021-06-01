# !/usr/bin/env python3
# -*- config: utf-8 -*-

from tkinter import *

if __name__ == '__main__':
    root = Tk()

    root.geometry('570x400')
    root.title("Подсистема управления процессами с переменной длительностью кванта")
    root.resizable(False, False)

    lb1 = Label(text='Командная срока', width=0)
    lb2 = Label(text='Терминал', width=0)
    en1 = Entry(width=68)
    term = Text(bg='white', width=65, height=19)

    lb1.grid(row=0, column=0, sticky=W, pady=10, padx=5)
    lb2.grid(row=1, column=1, sticky=W)
    en1.grid(row=0, column=1, sticky=W)
    term.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    root.mainloop()
