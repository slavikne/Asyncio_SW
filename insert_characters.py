import asyncio
import random
from pprint import pprint

import asyncpg
from more_itertools import chunked
import insert_characters
import config
from get_characters import get_char_main




async def insert_characters(pool: asyncpg.Pool, character):
    query = 'INSERT INTO character (birth_year, eye_color, films, gender, hair_color' \
            ', height, homeworld, mass, name, skin_color, species, starships, vehicles)' \
            ' VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)'

    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, character)


async def main():
    characters_list = await get_char_main()
    # pprint(characters_list)
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    tasks = []
    for users_chunk in chunked(characters_list, 10):
        tasks.append(asyncio.create_task(insert_characters(pool, users_chunk)))

    await asyncio.gather(*tasks)
    await pool.close()
#
if __name__ == '__main__':
    asyncio.run(main())