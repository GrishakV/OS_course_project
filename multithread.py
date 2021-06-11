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
            print_factors(x, quantum, res_list, quantum_list)

        time.sleep(1)


def print_factors(x, quantum, res_list, quantum_list):
    res_str = f'Квант = {idx[x]}с Множители числа {x}: '
    try:
        for k in quantums:
            quantum_list = k[x]
    except KeyError:
        quantum_list = []
    quantum_dic = {}
    quantum_list.append(idx[x])
    quantum_dic[x] = quantum_list
    quantums[:] = [d for d in quantums if d.get(x) == x]
    quantums.append(quantum_dic)
    try:
        print(quantums[x])
    except IndexError:
        print()
    try:
        for g in results:
            res_list = g[x]
    except KeyError:
        res_list = []
    res_dict = {}
    current_res = []
    st = time.time()
    try:
        begin = drop_list[x]
    except KeyError:
        begin = 1
    for i in range(begin, x+1):
        current = time.time()
        if i == x:
            del idx[x]
        if quantum < 8.0:
            if x % i == 0:
                current_res.append(i)
            elif (current - st) > quantum:
                idx[x] *= 2
                ps_queue.put(x)
                res_dict[x] = res_list + current_res
                drop_list[x] = i
                results[:] = [d for d in results if d.get(x) == x]
                results.append(res_dict)
                term.insert(END, f'Поток числа {x} превысил квант и отправлен обратно в очередь \n')
                break
        elif quantum == 8.0:
            if x % i == 0:
                current_res.append(i)
            elif (current - st) >= quantum:
                ps_queue.put(x)
                res_dict[x] = res_list + current_res
                drop_list[x] = i
                results[:] = [d for d in results if d.get(x) == x]
                results.append(res_dict)
                term.insert(END, f'Поток числа {x} превысил квант и отправлен обратно в очередь \n')
                break
    try:
        q_sum = sum(quantum_list)
        term.insert(END, f'Общее время выполнения = {q_sum}с \n')
    except IndexError:
        term.insert(END, f'[0.5c]')

    total_res = res_list + current_res
    for j in total_res:
        res_str += str(j) + ' '
    res_str += '\n'
    res_str += '-----------------------------------------------------------------\n'
    term.insert(END, res_str)


def entry_get(event):
    global idx, cm_list, ps_queue
    command = en1.get()
    term.insert(END, f'# {command} \n')
    cm_list.append(command)
    en1.delete(0, 'end')
    if command == 'exit':
        root.destroy()
    elif command.startswith('add '):
        parts = command.split(' ', maxsplit=3)
        num = int(parts[1])
        quant = float(0.5)
        idx[num] = quant
        ps_queue.put(num)
    elif command == 'clear':
        term.delete(0.0, END)
    elif command == 'start':
        thread1 = QueueThread('A')
        thread2 = QueueThread('B')
        thread1.start()
        thread2.start()
    elif command == 'list':
        term.insert(END, f'Список чисел для выделения множителей \n')
        for i in idx:
            term.insert(END, f'{i} \n')
    elif command == 'help':
        term.insert(END, f'"add ЧИСЛО" - добавляет ЧИСЛО для выделени-я множителя из него. \n')
        term.insert(END, f'"list" - выводит список чисел для выделения множителей. \n')
        term.insert(END, f'"clear" - очищает терминал. \n')
        term.insert(END, f'"help" - выводт список команд с кратким описанием. \n')
        term.insert(END, f'"start" - выделяет множетели из чисел и выводит их в терминал. \n')
        term.insert(END, f'"exit" - закрывает программу. \n')
    else:
        term.insert(END, f'{command} -- неизвестная комманда, используйте "help". \n')


if __name__ == '__main__':
    idx = {4141212: 0.5, 42192: 0.5}
    quantums = []
    quantum_list = []
    res_list = []
    results = []
    drop_list = {}
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

    lb1.grid(row=0, column=0, sticky=W, pady=10, padx=5)
    lb2.grid(row=1, column=1, sticky=W)
    en1.grid(row=0, column=1, sticky=W)
    term.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    root.mainloop()
