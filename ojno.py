#!/usr/bin/env python3
# -*- config: utf-8 -*-

import queue
import threading
import time


class MyThread(threading.Thread):
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
            res_str += str(i) + '; '
        if (current - st) > quantum:
            idx[x] *= 2
            ps_queue.put(x)
            res_str = f'Поток числа {x} превысил квант и отправлен обратно в очередь'
            break

    print(res_str)


if __name__ == '__main__':
    # idx = list(map(int, input("Введите список чисел для проверки:").split(' ')))
    idx = {1: 0.5, 3: 0.5, 11: 0.5, 19: 0.5, 33: 0.5, 57: 0.5, 131: 0.5, 209: 0.5,
           393: 0.5, 627: 0.5, 1441: 0.5, 2489: 0.5, 4323: 0.5, 7467: 0.5, 27379: 0.5, 82137: 0.5}
    print(idx)
    ps_queue = queue.Queue()
    for x in idx:
        ps_queue.put(x)

    thread1 = MyThread('A')
    thread2 = MyThread('B')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print('Done.')
