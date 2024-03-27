from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from src.exceptions import S3UploadException


def http_500_s3_file_upload_exception(request: Request, exception: S3UploadException):
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"message": f"Error uploading route geometries to S3!"})


def http_500_unknown_exception(request: Request, exception: Exception):
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"message": f"Unknown Error Occurred!"})


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(S3UploadException, http_500_s3_file_upload_exception)

    app.add_exception_handler(Exception, http_500_unknown_exception)
