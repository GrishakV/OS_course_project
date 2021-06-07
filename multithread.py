#!/usr/bin/env python3
# -*- config: utf-8 -*-

from tkinter import *
import queue
import threading
import time


class QueueThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self) -> None:
        print(f'Старт потока {self.name}')
        process_queue()
        print(f'Завершение потока {self.name}')


def process_queue():
    while True:
        try:
            x = ps_queue.get(block=False)
            quantum = idx[x]
        except queue.Empty:
            return
        else:
            print_factors(x, quantum)

        time.sleep(1)


def print_factors(x, quantum):
    res_str = f'Квант = {idx[x]}с Множители числа {x}: '
    st = time.time()
    for i in range(1, x+1):
        current = time.time()
        if x % i == 0:
            time.sleep(0.1)
            res_str += str(i) + ' '
            # term.insert(END, res_str)
        if (current - st) > quantum:
            idx[x] *= 2
            ps_queue.put(x)
            res_str = f'Поток числа {x} превысил квант и отправлен обратно в очередь'
            # term.insert(END, res_str)
            break
    print(res_str)


def entry_get(event):
    global idx, cm_list, ps_queue
    command = en1.get()
    cm_list.append(command)
    en1.delete(0, 'end')
    if command == 'exit':
        root.destroy()
    elif command.startswith('add '):
        parts = command.split(' ', maxsplit=3)
        num = int(parts[1])
        quant = float(parts[2])
        idx[num] = quant
        ps_queue.put(num)
    elif command == 'clear':
        term.delete(0.0, END)
    elif command == 'start':
        thread1 = QueueThread('A')
        thread2 = QueueThread('B')
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        print('Done.')
    elif command == 'list':
        for i in idx:
            term.insert(END, '{:>4}: {} \n'.format(i, idx[i]))


if __name__ == '__main__':
    idx = {4141212: 1.0, 42192: 0.1}
    cm_list = []
    ps_queue = queue.Queue()
    for x in idx:
        ps_queue.put(x)

    root = Tk()

    root.geometry('570x400')
    root.title("Подсистема управления процессами с переменной длительностью кванта")
    root.resizable(False, False)

    lb1 = Label(text='Командная срока', width=0)
    lb2 = Label(text='Терминал', width=0)
    en1 = Entry(width=68)
    term = Text(bg='white', width=65, height=19)

    en1.bind('<Return>', entry_get)
    en1.bind('<Button-1>', lambda x: print(idx))

    lb1.grid(row=0, column=0, sticky=W, pady=10, padx=5)
    lb2.grid(row=1, column=1, sticky=W)
    en1.grid(row=0, column=1, sticky=W)
    term.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    root.mainloop()

