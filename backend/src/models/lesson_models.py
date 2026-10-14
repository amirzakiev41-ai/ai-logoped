from dataclasses import dataclass


@dataclass
class LessonResult:
    recognized_word: str
    status: str
    score: float

@dataclass
class ScoreResult:
    status: str
    score: float

@dataclass
class LessonWord:
    word: str
    letter: str

@dataclass
class UserID:
    user_id: int