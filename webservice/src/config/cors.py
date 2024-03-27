import os
from pprint import pformat
from typing import Dict
from loguru import logger


allowed_origins = []

if os.environ.get('ORIGINS', ''):
    origins = os.environ.get('ORIGINS', '').split(';')
    allowed_origins.extend(origins)
    logger.info(f"Allowed origins:\n {pformat(allowed_origins)}")

else:
    allowed_origins.extend([
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://localhost:4000"
    ])


cors_configuration: Dict = {
    'allow_origins': allowed_origins,
    'allow_credentials': True,
    'allow_methods': ["*"],
    'allow_headers': ["*"]
}
