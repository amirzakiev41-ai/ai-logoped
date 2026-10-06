from fastapi import APIRouter, Request

from schemas.lesson_schemas import *


router = APIRouter(prefix="/lesson", tags=["lessons"])

@router.get("/{word_index}", response_model=LessonWordResponse)
def get_word(request: Request, word_index: int) -> LessonWordResponse:
    """
    Возвращает слово урока по его индексу.
    """
    container = request.app.state.container
    return container.word_service.get_word(word_index)


@router.post("/check")
def check_pronunciation(
    request: Request,
    body: CheckPronunciationRequest,
):
    container = request.app.state.container

    # Проверка пользователя
    container.user_service.get_user_by_id(body.user_id)

    word_letter = container.word_service.get_word(body.word_index)

    return container.lesson_service.check_pronunciation(
        user_id=body.user_id,
        word_letter=word_letter,
    )