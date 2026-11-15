import importlib.resources
import os.path
import re
from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import Set
from typing import Tuple

import pandas as pd
from loguru import logger
from pandas import DataFrame

from src.config.csvfiles import GTFS_DATA_ENCODING
from src.config.csvfiles import GTFS_RAW_CSV_FILE_READ_OPTIONS
from src.config.csvfiles import GTFS_RAW_STOP_TIMES_CSV_FILE_READ_OPTIONS
from src.config.csvfiles import GTFS_RESOURCE_PATH
from src.config.logging import configure_logger

TIME_FORMATS_REGEX_MATCHER = r'(\d{2}):(\d{2}):(\d{2})'
BROKEN_TIME_FORMATS_REGEX_MATCHER = r'((?<!2[0-3])\d{2}):(\d{2}):(\d{2})'

BUS_ROUTE_TYPE: str = '3'
LATITUDE_BOUNDS: Tuple[float, float] = (40.5, 41.8)
LONGITUDE_BOUNDS: Tuple[float, float] = (27.5, 30.0)

DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
WEBSERVICE_PROJECT_ROOT_PATH: str = os.path.join(DIR_PATH, '..')

ROUTES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'routes.csv').__str__()
TRIPS_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'trips.csv').__str__()
STOPS_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'stops.csv').__str__()
STOP_TIMES_CSV_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, 'stop_times.csv').__str__()


def is_timestamp_broken(time_str):
    return re.match(BROKEN_TIME_FORMATS_REGEX_MATCHER, time_str)


def fix_broken_timestamp(time_str):
    if pd.isna(time_str) or time_str == '':
        return None

    match = re.match(TIME_FORMATS_REGEX_MATCHER, time_str)

    if not match:
        return time_str

    today: datetime = datetime.today()
    hours, minutes, seconds = map(int, match.groups())
    is_next_day: bool = True if hours >= 24 else False
    correct_hour: int = hours % 24 if is_next_day else hours
    correct_day: int = (today + timedelta(days=1)).day if is_next_day else today.day

    time = datetime(
        year=today.year,
        month=today.month,
        day=correct_day,
        hour=correct_hour,
        minute=minutes,
        second=seconds
    )

    return time


def repair_double_encoded_text(text: str) -> str:
    if not text:
        return text

    try:
        return bytes(_to_cp1252_byte(char) for char in text).decode('utf-8')
    except (UnicodeDecodeError, ValueError):
        return text


def normalize_coordinate(value: str, bounds: Tuple[float, float]) -> Optional[float]:
    lower, upper = bounds
    candidate: str = value.split(':')[0].strip()
    if not candidate or 'E+' in candidate.upper():
        return None

    try:
        coordinate = float(candidate)
    except ValueError:
        digits = re.sub(r'\D', '', candidate)
        if len(digits) < 3:
            return None
        coordinate = float(f'{digits[:2]}.{digits[2:]}')

    if lower <= coordinate <= upper:
        return coordinate

    return None


def preprocess_routes():
    routes: DataFrame = pd.read_csv(ROUTES_CSV_PATH, **GTFS_RAW_CSV_FILE_READ_OPTIONS)
    has_route_id = routes['route_id'].str.fullmatch(r'\d+')
    logger.warning(f'Dropping {(~has_route_id).sum()} route rows without route_id (spill-over of multi-line descriptions)')
    routes = routes[has_route_id].copy()
    is_shifted = routes['route_type'] == ''
    logger.warning(f'Resetting {is_shifted.sum()} route rows shifted by a ";" in route_long_name: {routes.loc[is_shifted, "route_id"].tolist()}')
    routes.loc[is_shifted, ['route_type', 'route_desc', 'route_code']] = [BUS_ROUTE_TYPE, '', '']
    for column in ('route_long_name', 'route_desc'):
        routes[column] = routes[column].apply(repair_double_encoded_text)
    routes.to_csv(_clean_csv_path('routes.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)
    logger.info(f'Preprocessed {routes.shape[0]} routes')


def preprocess_trips():
    trips: DataFrame = pd.read_csv(TRIPS_CSV_PATH, **GTFS_RAW_CSV_FILE_READ_OPTIONS)
    trips.to_csv(_clean_csv_path('trips.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)
    logger.info(f'Preprocessed {trips.shape[0]} trips')


def preprocess_stops() -> Set[str]:
    stops: DataFrame = pd.read_csv(STOPS_CSV_PATH, **GTFS_RAW_CSV_FILE_READ_OPTIONS)
    stops = stops.loc[:, ~stops.columns.str.startswith('Unnamed')]
    stops['stop_lat'] = stops['stop_lat'].apply(lambda value: normalize_coordinate(value, LATITUDE_BOUNDS))
    stops['stop_lon'] = stops['stop_lon'].apply(lambda value: normalize_coordinate(value, LONGITUDE_BOUNDS))
    is_located = stops['stop_lat'].notna() & stops['stop_lon'].notna()
    logger.warning(f'Dropping {(~is_located).sum()} stops without usable coordinates: {stops.loc[~is_located, "stop_id"].tolist()}')
    stops = stops[is_located]
    stops.to_csv(_clean_csv_path('stops.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)
    logger.info(f'Preprocessed {stops.shape[0]} stops')

    return set(stops['stop_id'])


def preprocess_stop_times(stop_ids: Set[str]):
    stop_times: DataFrame = pd.read_csv(STOP_TIMES_CSV_PATH, **GTFS_RAW_STOP_TIMES_CSV_FILE_READ_OPTIONS)
    has_stop = stop_times['stop_id'].isin(stop_ids)
    logger.warning(f'Dropping {(~has_stop).sum()} stop_times of dropped stops')
    stop_times = stop_times[has_stop].copy()
    stop_times['arrival_time'] = stop_times['arrival_time'].apply(fix_broken_timestamp)
    stop_times['departure_time'] = stop_times['departure_time'].apply(fix_broken_timestamp)
    stop_times.to_csv(_clean_csv_path('stop_times.clean.csv'), index=False, encoding=GTFS_DATA_ENCODING)
    logger.info(f'Preprocessed {stop_times.shape[0]} stop_times')


def main():
    configure_logger()
    preprocess_routes()
    preprocess_trips()
    stop_ids = preprocess_stops()
    preprocess_stop_times(stop_ids)


def _clean_csv_path(filename: str) -> str:
    return os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'), filename)


def _to_cp1252_byte(char: str) -> int:
    try:
        return char.encode('cp1252')[0]
    except UnicodeEncodeError:
        if ord(char) < 256:
            return ord(char)
        raise ValueError(char)


if __name__ == '__main__':
    main()
