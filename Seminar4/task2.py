import requests
from multiprocessing import Process
import time

urls = ['https://www.google.ru/',
'https://gb.ru/',
'https://ya.ru/',
'https://www.python.org/',
'https://habr.com/ru/all/'
]


def get_urls(url):
    response = requests.get(url)
    filename = 'threads_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(f'task2dir/{filename}', 'w', encoding='utf-8') as file:
        file.write(response.text)


start_time = time.time()
processes = []

if __name__ == "__main__":
    for url in urls:
        process = Process(target=get_urls, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
        print(time.time() - start_time)
