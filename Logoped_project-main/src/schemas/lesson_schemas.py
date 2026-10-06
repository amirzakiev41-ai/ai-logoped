from pydantic import BaseModel, Field


class LessonWordResponse(BaseModel):
    word: str = Field(max_length=15)
    letter: str = Field(max_length=1)


class LessonResultResponse(BaseModel):
    recognized_word: str = Field(max_length=15)
    status: str
    score: float


class CheckPronunciationRequest(BaseModel):
    user_id: int = Field(ge=0)
    word_index: int = Field(ge=0)