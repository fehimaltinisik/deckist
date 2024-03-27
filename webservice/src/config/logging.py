from sys import stdout

from loguru import logger

FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n"  # noqa


def formatter(record):
    fmt = "{time:YYYY-MM-DD HH:mm:ss.SSS}| {level: <8} |"
    name = record['name']
    module_tree = name.split('.')
    record['name'] = '.'.join(module[0] for module in module_tree)

    if 'route_short_name' in record.get('extra'):
        fmt += " rSN:{extra[route_short_name]:^5} |"

    if 'route_id' in record.get('extra'):
        fmt += " routeId:{extra[route_id]:^7} |"

    if 'trip_id' in record.get('extra'):
        fmt += " tripId:{extra[trip_id]:^9} |"

    fmt += " {name}:{function}:{line} - <level>{message}</level>\n"
    if record.get('exception') is not None:
        fmt += "{exception}"

    return fmt


def configure_logger():
    logger.remove()
    logger.add(stdout, format=formatter, level="DEBUG", colorize=False)
