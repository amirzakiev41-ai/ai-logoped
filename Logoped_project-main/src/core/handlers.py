import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import *


ERROR_CODES = {

    WordNotFoundError: 404,
    UserNotFoundError: 404,
    ResultNotFoundError: 404,
    AudioFileNotFoundError: 404,

    InvalidUserDataError: 400,

    InvalidPasswordError: 401,

    DatabaseConnectionError: 500,
    DatabaseReadError: 500,
    DatabaseWriteError: 500,
    DatabaseDeleteError: 500,

    WhisperModelError: 500,
    SpeechRecognitionError: 500,
    WordSaveError: 500,
}


def register_exception_handlers(app: FastAPI):

    async def handler(request: Request, exc) -> JSONResponse | None:

        status = ERROR_CODES.get(type(exc), 500)

        return JSONResponse(
            status_code=status,
            content={
                "detail": str(exc)
            }
        )

    for error in ERROR_CODES:
        app.add_exception_handler(error, handler)

    @app.exception_handler(Exception)
    async def unknown(request: Request, exc) -> JSONResponse:

        traceback.print_exception(type(exc), exc, exc.__traceback__)

        return JSONResponse(
            status_code=500,
            content={"detail": "Внутренняя ошибка сервера"},
        )
    
    @app.exception_handler(UnsupportedLetterError)
    async def unsupported_letter_handler(request: Request, exc: UnsupportedLetterError,):
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc),
            },
        )