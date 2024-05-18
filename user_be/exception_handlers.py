import logging
from http import HTTPStatus

from fastapi import Request, Response, FastAPI
from fastapi.exception_handlers import request_validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException

from user_be import exceptions

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: exceptions.ValidationException) -> Response:
    return await request_validation_exception_handler(
        request=request,
        exc=RequestValidationError(errors=[exc])
    )


async def does_not_exist_exception_handler(request: Request, exc: exceptions.DoesNotExistException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc))
    )


async def already_exist_exception_handler(request: Request, exc: exceptions.AlreadyExistException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(exc))
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(exceptions.ValidationException)(validation_exception_handler)
    app.exception_handler(exceptions.DoesNotExistException)(does_not_exist_exception_handler)
    app.exception_handler(exceptions.AlreadyExistException)(already_exist_exception_handler)
