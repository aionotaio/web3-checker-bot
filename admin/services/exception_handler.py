from fastapi import Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from docker.errors import NotFound, APIError
from aiogram.exceptions import TelegramBadRequest

from shared.exceptions import TokenValidationError, EmptyError, WrongCredentialsError, MissingError



async def empty_error_handler(request: Request, exc: EmptyError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def token_validation_error_handler(request: Request, exc: TokenValidationError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def wrong_creds_error_handler(request: Request, exc: WrongCredentialsError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def missing_error_handler(request: Request, exc: MissingError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def telegram_bad_request_error_handler(request: Request, exc: TelegramBadRequest):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def docker_not_found_error_handler(request: Request, exc: NotFound):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def docker_api_error_handler(request: Request, exc: APIError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


async def other_error_handler(request: Request, exc: Exception):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
