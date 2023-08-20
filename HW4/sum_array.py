import asyncio
import threading
from multiprocessing import Process, Value
from random import randint
from time import time


def find_sum_sync(array):
    return sum(array)


def find_sum_thread(array):
    num_threads = 4
    chunk_size = len(array) // num_threads
    threads = []
    results = []

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(array)
        thread = threading.Thread(target=lambda r, a: r.append(find_sum_sync(a[start:end])), args=(results, array))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)


def sum_proc(result, array):
    result.value = sum(array)


def find_sum_proc(array):
    num_processes = 4
    chunk_size = len(array) // num_processes
    processes = []
    results = []

    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(array)
        result = Value('i', 0)
        process = Process(target=sum_proc, args=(result, array[start:end]))
        processes.append(process)
        results.append(result)
        process.start()

    for process in processes:
        process.join()

    return sum(r.value for r in results)


async def find_sum_async(array):
    return sum(array)


async def main_async(array):
    num_tasks = 4
    chunk_size = len(array) // num_tasks
    tasks = []

    for i in range(num_tasks):
        start = i * chunk_size
        end = start + chunk_size if i < num_tasks - 1 else len(array)
        tasks.append(find_sum_async(array[start:end]))

    results = await asyncio.gather(*tasks)
    return sum(results)


if __name__ == "__main__":
    arr = [randint(1, 100) for _ in range(1_000_000)]

    for func in (find_sum_sync, find_sum_thread, find_sum_proc, main_async):
        start_time = time()
        if func in (find_sum_sync, find_sum_thread, find_sum_proc):
            res = func(arr)
        else:
            res = asyncio.run(main_async(arr))
        end_time = time()
        print(f'{func.__name__.split("_")[-1]}:\n   res: {res}\n   time: {end_time - start_time:.3f}')
