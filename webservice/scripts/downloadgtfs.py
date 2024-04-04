import os.path
import shutil

import importlib.resources
from io import BytesIO

import urllib3
from loguru import logger

from src.config.csvfiles import GTFS_RESOURCE_PATH
from src.config.logging import configure_logger

DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
WEBSERVICE_PROJECT_ROOT_PATH: str = os.path.join(DIR_PATH, '..')

GTFS_TRIPS_DATA_URL = "https://data.ibb.gov.tr/en/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/7ff49bdd-b0d2-4a6e-9392-b598f77f5070/download/trips.csv"
GTFS_STOPS_DATA_URL = "https://data.ibb.gov.tr/en/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/2299bc82-983b-4bdf-8520-5cef8c555e29/download/stops.csv"
GTFS_STOP_TIMES_DATA_URL = "https://data.ibb.gov.tr/en/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/23778613-16fe-4d30-b8b8-8ca934ed2978/download/stop_times.csv"
GTFS_ROUTES_DATA_URL = "https://data.ibb.gov.tr/en/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/46dbe388-c8c2-45c4-ac72-c06953de56a2/download/routes.csv"


def create_resources_directories_if_not_exists():
    path = os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'))
    if not os.path.exists(os.path.join(path)):
        logger.info(f'Creating directory: {GTFS_RESOURCE_PATH}')
        os.makedirs(path, exist_ok=True)


create_resources_directories_if_not_exists()


GTFS_DATA_SAVE_PATH: str = importlib.resources.path(GTFS_RESOURCE_PATH, '').__str__()


def download_file(http_client, url, encoding):
    filename = url.split('/')[-1]
    logger.debug(f'Downloading file: {filename}...')
    with (
        http_client.request('GET', url, preload_content=False) as response,
        open(os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_DATA_SAVE_PATH.split('.'), filename), 'wb') as file
    ):
        content = response.read().decode(encoding)
        content = content.encode('UTF-16LE')
        buffer = BytesIO()
        buffer.write(content)
        buffer.seek(0)

        shutil.copyfileobj(buffer, file)

    logger.info(f'File downloaded: {filename}')


def main():
    configure_logger()
    http_client = urllib3.PoolManager()
    download_file(http_client, GTFS_TRIPS_DATA_URL, 'windows-1254')
    download_file(http_client, GTFS_STOPS_DATA_URL, 'windows-1254')
    download_file(http_client, GTFS_STOP_TIMES_DATA_URL, 'utf-8')
    download_file(http_client, GTFS_ROUTES_DATA_URL, 'utf-8')

    exit()


if __name__ == '__main__':
    main()
