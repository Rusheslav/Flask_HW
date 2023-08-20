import threading
import requests
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
    with open(f'task1dir/{filename}', 'w', encoding='utf-8') as file:
        file.write(response.text)


start_time = time.time()
threads = []

for url in urls:
    thread = threading.Thread(target=get_urls, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
    print(time.time() - start_time)
