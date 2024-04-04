import csv
import importlib.resources

import numpy as np
import pandas as pd
from loguru import logger
from pandas import DataFrame
from tortoise import run_async

from src.clients import TortoiseOrm
from src.config.csvfiles import GTFS_DATA_CSV_FILE_READ_OPTIONS
from src.config.csvfiles import GTFS_RESOURCE_PATH
from src.repositories import route_repository
from src.repositories import shape_repository
from src.repositories import stop_repository
from src.repositories import trip_repository
from src.repositories import stop_time_repository


ROUTES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'routes.clean.csv').__str__()
SHAPES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'shapes.csv').__str__()
TRIPS_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'trips.clean.csv').__str__()
STOPS_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'stops.clean.csv').__str__()
STOP_TIMES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'stop_times.clean.csv').__str__()

logger.debug("Found all GTFS resources...")


async def save_routes(batch_size: int = 1000):
    routes: DataFrame = pd.read_csv(
        ROUTES_CSV_PATH,
        dtype={
            'route_id': int,
            'route_short_name': str,
            'route_long_name': str
        },
        converters={'route_desc': str},
        **GTFS_DATA_CSV_FILE_READ_OPTIONS
    )
    logger.info("Read routes from CSV...")
    logger.info('Saving routes to SQLite...')
    n_of_records: int = routes.shape[0]
    for i, (_, batch) in enumerate(routes.groupby(np.arange(n_of_records) // batch_size)):
        logger.debug(f'{i}. route batch shape:{batch.shape}')
        await route_repository.create_many(batch.to_dict('records'))
        logger.debug(f'{i}. route batch saved successfully!')
    logger.info('Routes saved to SQLite successfully!')


async def save_shapes(batch_size: int = 1000):
    shapes: DataFrame = pd.read_csv(
        SHAPES_CSV_PATH,
        **{
            'encoding': 'windows-1254',
            'sep': ',',
            'quotechar': '"',
            'quoting': csv.QUOTE_ALL
        }
    )
    logger.info("Read shapes from CSV...")
    logger.info('Saving shapes to SQLite...')
    n_of_records = shapes.shape[0]
    for i, (_, batch) in enumerate(shapes.groupby(np.arange(n_of_records) // batch_size)):
        logger.debug(f'{i}. shape batch shape:{batch.shape}')
        await shape_repository.create_many(batch.to_dict('records'))
        logger.debug(f'{i}. shape batch saved successfully!')
    logger.info('Shapes saved to SQLite successfully!')


async def save_trips(batch_size: int = 1000):
    trips: DataFrame = pd.read_csv(
        TRIPS_CSV_PATH,
        **GTFS_DATA_CSV_FILE_READ_OPTIONS
    )
    logger.info("Read trips from CSV...")
    logger.info('Saving trips to SQLite...')
    n_of_records = trips.shape[0]
    for i, (_, batch) in enumerate(trips.groupby(np.arange(n_of_records) // batch_size)):
        logger.debug(f'{i}. trip batch shape:{batch.shape}')
        batch['direction_id'] = batch['direction_id'].astype('Int64')
        await trip_repository.create_many(batch.to_dict('records'))
        logger.debug(f'{i}. trip batch batch saved successfully!')
    logger.info('Trips saved to SQLite successfully!')


async def save_stops(batch_size: int = 1000):
    stops: DataFrame = pd.read_csv(
        STOPS_CSV_PATH,
        **GTFS_DATA_CSV_FILE_READ_OPTIONS
    )
    logger.info("Read stops from CSV...")
    logger.info('Saving stops to SQLite...')
    n_of_records = stops.shape[0]
    for i, (_, batch) in enumerate(stops.groupby(np.arange(n_of_records) // batch_size)):
        logger.debug(f'{i}. stop batch shape:{batch.shape}')
        await stop_repository.create_many(batch.to_dict('records'))
        logger.debug(f'{i}. stop batch saved successfully!')
    logger.info('Stops saved to SQLite successfully!')


async def save_stop_times(batch_size: int = 1000):
    stop_times: pd.DataFrame = pd.read_csv(
        STOP_TIMES_CSV_PATH,
        parse_dates=['arrival_time', 'departure_time'],
        date_parser=pd.to_datetime,
        **GTFS_DATA_CSV_FILE_READ_OPTIONS
    )
    logger.info('Saving stop_times to SQLite...')
    n_of_records = stop_times.shape[0]
    for i, (_, batch) in enumerate(stop_times.groupby(np.arange(n_of_records) // batch_size)):
        logger.debug(f'{i}. stop_times batch shape:{batch.shape}')
        batch.replace(
            {
                'arrival_time': {pd.NaT: None},
                'departure_time': {pd.NaT: None}
            },
            inplace=True
        )
        await stop_time_repository.create_many(batch.to_dict('records'))
        logger.debug(f'{i}. stop_times batch saved successfully!')
    logger.info('Stop_times saved to SQLite successfully!')


async def run():
    logger.info('Saving GTFS resources to SQLite...')
    await TortoiseOrm.init()
    await save_routes()
    # await save_shapes()
    await save_trips()
    await save_stops()
    await save_stop_times()
    await TortoiseOrm.close()
    logger.info('GTFS resources saved to SQLite successfully!')


if __name__ == "__main__":
    run_async(run())

