from fastapi import APIRouter

from api.lesson import router as lesson_router
from api.statistics import router as statistic_router
from api.users import router as user_router


main_router = APIRouter()

main_router.include_router(lesson_router)
main_router.include_router(statistic_router)
main_router.include_router(user_router)
#fj
