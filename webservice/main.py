import os
import uvicorn


HOST = os.environ.get("HOST", "0.0.0.0")
LOG_LEVEL = str.lower(os.environ.get("LOG_LEVEL", "error"))
RELOAD_UVICORN = bool(int(os.environ.get("RELOAD_UVICORN", "0")))


if __name__ == '__main__':
    uvicorn.run(
        app="src.webserver:app",
        host=HOST,
        port=8000,
        log_level=LOG_LEVEL,
        reload=RELOAD_UVICORN
    )
