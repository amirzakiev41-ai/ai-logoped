from fastapi import APIRouter, Request

from schemas.statistic_schemas import GeneralStatisticsResponse, LetterStatisticsResponse, AllLettersStatisticsResponse


router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@router.get("/{user_id}", response_model=GeneralStatisticsResponse)
def get_general_statistics(
    request: Request,
    user_id: int,
) -> GeneralStatisticsResponse:

    container = request.app.state.container

    return container.statistics_service.get_general_statistics(user_id)


@router.get("/{user_id}/letters", response_model=AllLettersStatisticsResponse)
def get_all_statistics_of_letters(
    request: Request,
    user_id: int,
) -> AllLettersStatisticsResponse:

    container = request.app.state.container

    return AllLettersStatisticsResponse(
        letters=container.statistics_service.get_all_statistics_of_letters(user_id)
    )


@router.get("/{user_id}/letters/{letter}", response_model=LetterStatisticsResponse)
def get_statistics_by_letter(
    request: Request,
    user_id: int,
    letter: str,
) -> LetterStatisticsResponse:

    container = request.app.state.container

    return container.statistics_service.get_statistics_by_letter(
        user_id=user_id,
        letter=letter,
    )
