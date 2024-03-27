# IETT_RESOURCES_PATH: str = 'src.resources.samples'
import csv

GTFS_RESOURCE_PATH: str = 'src.resources.gtfs'
GTFS_DATA_ENCODING: str = 'UTF-16LE'
GTFS_DATA_CSV_FILE_READ_OPTIONS: dict = {
    'encoding': GTFS_DATA_ENCODING,
    'sep': ',',
    'quotechar': '"',
    'quoting': csv.QUOTE_ALL
}
