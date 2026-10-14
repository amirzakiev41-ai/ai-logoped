from fastapi import APIRouter, Request, UploadFile, File, Form

from schemas.lesson_schemas import *


router = APIRouter(prefix="/lesson", tags=["lessons"])


@router.get("/{word_index}", response_model=LessonWordResponse)
def get_word(request: Request, word_index: int) -> LessonWordResponse:
    """
    Возвращает слово урока по его индексу.
    """
    container = request.app.state.container
    return container.word_service.get_word(word_index)


@router.post("/check", response_model=LessonResultResponse)
async def check_pronunciation(
    request: Request,
    user_id: int = Form(...),
    word_index: int = Form(...),
    audio: UploadFile = File(...),
):
    container = request.app.state.container

    # Проверка пользователя
    container.user_service.get_user_by_id(user_id)

    # Получаем слово урока
    word_letter = container.word_service.get_word(word_index)

    # Передаём аудиофайл в сервис
    return await container.lesson_service.check_pronunciation(
        user_id=user_id,
        word_letter=word_letter,
        audio=audio,
    )