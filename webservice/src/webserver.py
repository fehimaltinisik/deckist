from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.clients import HTTPClient
from src.clients import TortoiseOrm
from src.config.cors import cors_configuration
from src.config.logging import configure_logger
from src.routers import route_router
from src.routers import routes_router
from src.routers import deck_router
from src.server.exceptionfilters import register_exception_handlers


configure_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await HTTPClient.init()
    await TortoiseOrm.init()

    yield

    await HTTPClient.close()
    await TortoiseOrm.close()


app = FastAPI(
    title="DeckIst API",
    docs_url="/docs",
    lifespan=lifespan     # noqa
)


app.add_middleware(CORSMiddleware, **cors_configuration)

register_exception_handlers(app)

app.include_router(route_router)
app.include_router(routes_router)
app.include_router(deck_router)


@app.get("/")
async def redirect_to_docs():
    response = RedirectResponse(url="/docs")

    return response
