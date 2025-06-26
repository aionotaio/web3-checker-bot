import logging.config

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from docker.errors import NotFound, APIError
from aiogram.exceptions import TelegramBadRequest

from api import users, bot, stats, auth
from pages import pages
from services.exception_handler import other_error_handler, empty_error_handler, missing_error_handler, docker_api_error_handler, wrong_creds_error_handler, docker_not_found_error_handler, token_validation_error_handler, telegram_bad_request_error_handler
from services.logging_config import LOGGING_CONFIG
from shared.vars import STATIC_DIR
from shared.exceptions import TokenValidationError, EmptyError, WrongCredentialsError, MissingError


logging.config.dictConfig(LOGGING_CONFIG)


app = FastAPI()

app.mount("/static", StaticFiles(directory=STATIC_DIR), "static")

app.include_router(users.router)
app.include_router(bot.router)
app.include_router(stats.router)
app.include_router(auth.router)
app.include_router(pages.router)

app.add_exception_handler(NotFound, docker_not_found_error_handler)
app.add_exception_handler(APIError, docker_api_error_handler)
app.add_exception_handler(TelegramBadRequest, telegram_bad_request_error_handler)
app.add_exception_handler(TokenValidationError, token_validation_error_handler)
app.add_exception_handler(EmptyError, empty_error_handler)
app.add_exception_handler(WrongCredentialsError, wrong_creds_error_handler)
app.add_exception_handler(MissingError, missing_error_handler)
app.add_exception_handler(Exception, other_error_handler)
