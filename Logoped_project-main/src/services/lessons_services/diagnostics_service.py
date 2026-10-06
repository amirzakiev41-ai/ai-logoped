import rapidfuzz
import difflib

from models.lesson_models import ScoreResult


class DiagnosticsService:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.words = self.settings.words
    
    def evaluate_score(self, expected_word: str, recognized_text: str) -> ScoreResult:
        score: float = rapidfuzz.fuzz.ratio(expected_word, recognized_text)
        
        if score == self.settings.COMPLETE_SCORE:
            check_results = ScoreResult("SUCCESS", score)
        elif score >= self.settings.ENOUGH_SCORE:
            check_results = ScoreResult("MISTAKE", score)
        else:
            check_results = ScoreResult("INVALID", score)
        
        return check_results
    
    def analyze_errors(self, expected_word: str, recognized_word: str) -> str:
        matcher = difflib.SequenceMatcher(None, expected_word, recognized_word)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "replace":
                return (f"Вы сказали {recognized_word} вместо {expected_word}. Возможны трудности с произношением звука '{expected_word[i1:i2]}'. Вместо '{expected_word[i1:i2]}' был распознан звук '{recognized_word[j1:j2]}'",
                        recognized_word[j1:j2], expected_word[i1:i2])
            elif tag == "insert":
                return (f"Вы сказали {recognized_word} вместо {expected_word}. Возможно добавление лишнего звука '{recognized_word[j1:j2]}' при произношении.",
                        recognized_word[j1:j2], expected_word[i1:i2])
            elif tag == "delete":
                return (f"Вы сказали {recognized_word} вместо {expected_word}. Возможно пропуск звука '{expected_word[i1:i2]}'.",
                        recognized_word[j1:j2], expected_word[i1:i2])
