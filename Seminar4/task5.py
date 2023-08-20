import asyncio
from os import walk
import time


async def count_words_in_dir(path):
    files = list(walk(path))[0][2]
    tasks = []
    for file in files:
        task = asyncio.ensure_future(count_words(f'{path}/{file}'))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def count_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        print(len(f.read().split()))
        print(f'Time: {time.time() - start_time}')


start_time = time.time()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(count_words_in_dir('task1dir'))
