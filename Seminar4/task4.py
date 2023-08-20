import threading
from os import walk
import time


def count_words_in_dir(path):
    files = list(walk(path))[0][2]
    threads = []
    for file in files:
        thread = threading.Thread(target=count_words, args=[f'{path}/{file}'])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def count_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        print(len(f.read().split()))
        print(f'Time: {time.time() - start_time}')


start_time = time.time()
count_words_in_dir('task1dir')
