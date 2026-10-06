from pydantic import BaseModel, ConfigDict, Field


class GeneralStatisticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    attempts_count: int = Field(ge=0)
    average_score: float | None
    success_count: int = Field(ge=0)


class LetterStatisticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    letter: str = Field(min_length=1, max_length=1)
    attempts_count: int = Field(ge=0)
    average_score: float | None
    success_count: int = Field(ge=0)


class AllLettersStatisticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    letters: list[LetterStatisticsResponse]