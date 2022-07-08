import asyncio
import aiohttp
import time
from more_itertools import chunked
from pprint import pprint

URL = 'https://swapi.dev/api/people/'

MAX = 100
PARTITION = 10
SLEEP_TIME = 1


async def health_check():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get('https://swapi.dev/api/', ssl=False) as response:
                    if response.status == 200:
                        print('OK')
                    else:
                        print(response.status)
            except Exception as er:
                print(er)
            await asyncio.sleep(1)


async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}', ssl=False) as response:
        return await response.json()


async def get_people(all_ids, partition, session):
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_person(person_id, session)) for person_id in chunk_ids]
        for task in tasks:
            task_result = await task
            yield task_result


async def get_char_main():
    health_check_task = asyncio.create_task(health_check())
    # print(health_check_task)
    list_characters = []
    async with aiohttp.ClientSession() as session:
        async for people in get_people(range(1, MAX +1), PARTITION, session):
            if len(people) == 16:
                list_characters.append([
                    people['birth_year'],
                    people['eye_color'],
                     ', '.join(map(str, people['films'])),
                     people['gender'],
                     people['hair_color'],
                     people['height'],
                     people['homeworld'],
                     people['mass'],
                     people['name'],
                     people['skin_color'],
                     ', '.join(map(str, people['species'])),
                     ', '.join(map(str, people['starships'])),
                     ', '.join(map(str, people['vehicles']))
                ])
        return list_characters
#     pprint(list_characters)
# start = time.time()
# asyncio.run(get_char_main())
# print(time.time() - start)



# list_characters.append({
#                     'birth_year': people['birth_year'],
#                     'eye_color': people['eye_color'],
#                     'films': ', '.join(map(str, people['films'])),
#                     'gender': people['gender'],
#                     'hair_color': people['hair_color'],
#                     'height': people['height'],
#                     'homeworld': people['homeworld'],
#                     'mass': people['mass'],
#                     'name': people['name'],
#                     'skin_color': people['skin_color'],
#                     'species': ', '.join(map(str, people['species'])),
#                     'starships': ', '.join(map(str, people['starships'])),
#                     'vehicles': ', '.join(map(str, people['vehicles']))
#                 })