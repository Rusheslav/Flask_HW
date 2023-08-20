import asyncio
import aiohttp
import time

urls = ['https://www.google.ru/',
'https://gb.ru/',
'https://ya.ru/',
'https://www.python.org/',
'https://habr.com/ru/all/'
]


async def get_urls(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = 'threads_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
            with open(f'task3dir/{filename}', 'w', encoding='utf-8') as file:
                file.write(text)
                print(f"Downloaded {url} in {time.time() - start_time: .2f} seconds")


async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(get_urls(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


start_time = time.time()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
