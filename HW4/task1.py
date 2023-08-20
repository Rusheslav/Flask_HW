# Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность,
# многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения
# вычислений.

import threading
from multiprocessing import Process, Value
from random import randint
from time import time

arr = [randint(1, 100) for _ in range(3_000_000)]


def find_sum_sync(array):
    global res
    for num in array:
        res += num


def find_sum_thread(array):
    threads = []
    num = 5
    for i in range(1, num + 1):
        thread = threading.Thread(target=find_sum_sync, args=[array[int(((i - 1) / num) * len(array)):
                                                                    int((i / num) * len(array))]])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def sum_proc(result, array):
    with result.get_lock():
        for num in array:
            result.value += num


def find_sum_proc(array):
    global res
    res = Value('i', 0)

    processes = []
    num = 4
    for i in range(1, num + 1):
        process = Process(target=sum_proc, args=(res, array[int(((i - 1) / num) * len(array)):
                                                            int((i / num) * len(array))]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    res = res.value


if __name__ == "__main__":
    for func in (find_sum_sync, find_sum_thread, find_sum_proc):
        res = 0
        start_time = time()
        func(arr)
        end_time = time()
        print(f'{func.__name__.split("_")[-1]}:\n   res: {res}\n   time: {end_time - start_time: .3f}')
