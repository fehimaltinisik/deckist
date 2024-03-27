import os
from enum import Enum

from loguru import logger
from tortoise import Tortoise


CONNECTION = os.environ.get('SQLITE_CONNECTION', 'gtfs.db')


class TortoiseOrm:
    class Table(str, Enum):
        ROUTE: str = 'route'

    @classmethod
    async def init(cls):
        logger.info("Connecting to SQLite database...")
        await Tortoise.init(
            db_url=f'sqlite://{CONNECTION}',
            modules={
                'models': ['src.entities.gtfs']
            }
        )
        logger.info("Initialized Tortoise ORM!")
        await Tortoise.generate_schemas()
        logger.info("Generated schemas!")
        logger.info("Connected to SQLite database!")

    @staticmethod
    async def close():
        logger.info("Closing connection to SQLite database...")
        await Tortoise.close_connections()
        logger.info("Connection to SQLite database closed!")
