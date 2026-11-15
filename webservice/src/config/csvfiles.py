# IETT_RESOURCES_PATH: str = 'src.resources.samples'
import csv
import os.path

WEBSERVICE_PROJECT_ROOT_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GTFS_RESOURCE_PATH: str = 'src.resources.gtfs'
GTFS_RESOURCE_DIRECTORY_PATH: str = os.path.join(WEBSERVICE_PROJECT_ROOT_PATH, *GTFS_RESOURCE_PATH.split('.'))
GTFS_RAW_DATA_ENCODING: str = 'utf-8-sig'
GTFS_RAW_CSV_FILE_READ_OPTIONS: dict = {
    'encoding': GTFS_RAW_DATA_ENCODING,
    'sep': ';',
    'dtype': str,
    'keep_default_na': False
}
GTFS_RAW_STOP_TIMES_CSV_FILE_READ_OPTIONS: dict = {
    **GTFS_RAW_CSV_FILE_READ_OPTIONS,
    'sep': ','
}
GTFS_DATA_ENCODING: str = 'utf-8'
GTFS_DATA_CSV_FILE_READ_OPTIONS: dict = {
    'encoding': GTFS_DATA_ENCODING,
    'sep': ',',
    'quotechar': '"',
    'quoting': csv.QUOTE_ALL
}
