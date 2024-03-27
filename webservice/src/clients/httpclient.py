import os
from typing import Dict
from typing import Literal
from typing import Optional
from urllib.parse import urljoin

from aiohttp import ClientSession
from aiohttp import ClientTimeout
from loguru import logger

from src.definitions.api import API


class HTTPClient:
    client: Optional[ClientSession]
    api_url_by_api_name: Dict[API, str] = {}

    @classmethod
    async def init(cls):
        timeout = ClientTimeout(total=1)
        cls.client = ClientSession(timeout=timeout)

    @classmethod
    async def close(cls):
        await cls.client.close()

    @classmethod
    async def request(
            cls,
            api: API,
            method: Literal['GET', 'DELETE', 'PUT', 'POST'],
            endpoint: str,
            *,
            body: Optional[Dict] = None,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None
    ) -> Optional[Dict]:
        base_url: str = cls.api_url_by_api_name.get(api)
        request_url: str = urljoin(base_url, endpoint)

        optionals_kwargs: Dict = {}
        if body:
            optionals_kwargs.update({'json': body})

        if params:
            optionals_kwargs.update({'params': params})

        if headers:
            optionals_kwargs.update({'headers': headers})

        try:
            response = await cls.client.request(method, request_url, **optionals_kwargs)
            logger.debug(f"HTTP request {method} {request_url} responded with status: {response.status}.")
            response.raise_for_status()

        except Exception as e:
            logger.exception(f"HTTP request {method} {request_url} raised: {e}.")

            return None

        else:
            return await response.json()
