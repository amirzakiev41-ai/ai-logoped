from dataclasses import dataclass
from models.lesson_models import LessonResult


@dataclass
class StatisticsResult:
    attempts_count: int
    average_score: float | None
    success_count: int


@dataclass
class LetterStatisticsResult:
    letter: str
    attempts_count: int
    average_score: float | None
    success_count: int


@dataclass
class SaveResultData:
    user_id: int
    expected_word: str
    main_letter: str
    lesson_result: LessonResult