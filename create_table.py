import asyncio
from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import config


engine = create_async_engine(config.PG_DSN_ALC, echo=True)
Base = declarative_base()



class Сharacter(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String, nullable=False)
    eye_color = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    hair_color = Column(String, nullable=False)
    height = Column(String, nullable=False)
    films = Column(String, nullable=False)
    homeworld = Column(String, nullable=False)
    mass = Column(String, nullable=False)
    name = Column(String, nullable=False)
    skin_color = Column(String, nullable=False)
    species = Column(String, nullable=False)
    starships = Column(String, nullable=False)
    vehicles = Column(String, nullable=False)


async def get_async_session(
    drop: bool = False, create: bool = False
):

    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print(1)
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def main():
    await get_async_session(True, True)


if __name__ == '__main__':
    asyncio.run(main())