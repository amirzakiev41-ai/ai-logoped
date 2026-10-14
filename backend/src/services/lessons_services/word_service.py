from core.config import Settings
from core.exceptions import WordNotFoundError
from models.lesson_models import LessonWord


class WordService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.words = self.settings.words

    def get_word(self, word_index: int) -> LessonWord:
            if not 0 <= word_index < len(self.words):
                raise WordNotFoundError("Word not found")
            
            return self.words[word_index]