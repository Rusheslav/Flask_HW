import threading
import requests
import time

urls = ['https://w.forfun.com/fetch/70/7047b702475924ba8f8044b5b5ca56ba.jpeg',
        'https://cdn.iportal.ru/preview/news/articles/5648d0f5489371e8bc21a22a5bcdf9a901239b4c_1032.jpg',
        'https://cs11.livemaster.ru/storage/topic/NxN/48/72/51ca01280af65e4ef909ed524902f4cfaf44vc.jpg',
        'https://4lapy.ru/resize/1664x1000/upload/medialibrary/270/2703fd71a17c0843c0b91bbe28c4fe0f.jpg',
        'https://s0.bloknot-voronezh.ru/thumb/850x0xcut/upload/iblock/509/0d1587dc21_7605080_8213488.jpg']


def get_urls(url):
    response = requests.get(url)
    filename = url.replace('https://', '').replace('.', '_').replace('/', '') + '.jpg'
    with open(f'task9dir/{filename}', 'wb') as file:
        file.write(response.content)


start_time = time.time()
threads = []

for url in urls:
    thread = threading.Thread(target=get_urls, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
    print(time.time() - start_time)
