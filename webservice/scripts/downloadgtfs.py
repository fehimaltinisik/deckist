import os.path
import shutil
import zipfile

import urllib3
from loguru import logger

from src.config.csvfiles import GTFS_RESOURCE_DIRECTORY_PATH
from src.config.csvfiles import GTFS_RESOURCE_PATH
from src.config.logging import configure_logger

GTFS_TRIPS_DATA_URL = "https://data.ibb.gov.tr/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/7ff49bdd-b0d2-4a6e-9392-b598f77f5070/download/trips.csv"
GTFS_STOPS_DATA_URL = "https://data.ibb.gov.tr/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/2299bc82-983b-4bdf-8520-5cef8c555e29/download/stops.csv"
GTFS_STOP_TIMES_ZIP_DATA_URL = "https://data.ibb.gov.tr/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/80401c1c-c240-4a32-8f40-ef697100a681/download/stop_times.zip"
GTFS_ROUTES_DATA_URL = "https://data.ibb.gov.tr/dataset/8540e256-6df5-4719-85bc-e64e91508ede/resource/46dbe388-c8c2-45c4-ac72-c06953de56a2/download/routes.csv"
ROUTE_PATHS_DATA_URL = "https://data.ibb.gov.tr/dataset/b48d2095-851c-413c-8d36-87d2310a22b5/resource/4ccb4d29-c2b6-414a-b324-d2c9962b18e2/download/iett-hat-guzergahlar-verisi.geojson"
ROUTE_PATHS_FILENAME = 'iett-hat-guzergahlari.geojson'


def create_resources_directories_if_not_exists():
    if not os.path.exists(GTFS_RESOURCE_DIRECTORY_PATH):
        logger.info(f'Creating directory: {GTFS_RESOURCE_PATH}')
        os.makedirs(GTFS_RESOURCE_DIRECTORY_PATH, exist_ok=True)


create_resources_directories_if_not_exists()


def download_file(http_client, url, filename=None) -> str:
    filename = filename or url.split('/')[-1]
    file_path = os.path.join(GTFS_RESOURCE_DIRECTORY_PATH, filename)
    logger.debug(f'Downloading file: {filename}...')
    with (
        http_client.request('GET', url, preload_content=False) as response,
        open(file_path, 'wb') as file
    ):
        shutil.copyfileobj(response, file)

    logger.info(f'File downloaded: {filename}')

    return file_path


def download_zipped_csv(http_client, url, member, filename):
    zip_path = download_file(http_client, url)
    with (
        zipfile.ZipFile(zip_path) as archive,
        archive.open(member) as source,
        open(os.path.join(GTFS_RESOURCE_DIRECTORY_PATH, filename), 'wb') as target
    ):
        shutil.copyfileobj(source, target)
    os.remove(zip_path)
    logger.info(f'File extracted: {member} as {filename}')


def main():
    configure_logger()
    http_client = urllib3.PoolManager()
    download_file(http_client, GTFS_TRIPS_DATA_URL)
    download_file(http_client, GTFS_STOPS_DATA_URL)
    download_zipped_csv(http_client, GTFS_STOP_TIMES_ZIP_DATA_URL, 'stop_times.txt', 'stop_times.csv')
    download_file(http_client, GTFS_ROUTES_DATA_URL)
    download_file(http_client, ROUTE_PATHS_DATA_URL, ROUTE_PATHS_FILENAME)

    exit()


if __name__ == '__main__':
    main()
