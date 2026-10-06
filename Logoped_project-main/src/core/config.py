from pathlib import Path

from models.lesson_models import LessonWord

class Settings:
    def __init__(self) -> None:
        self.words: list[LessonWord] = [
            LessonWord("рыба",  "р"),
            LessonWord("луна",  "л"),
            LessonWord("шар",   "ш"),
            LessonWord("сок",   "с"),
            LessonWord("трава", "р"),
        ]
        self.WORDS_NUM: int = len(self.words)
    
        self.MODEL: str = "small"
        
        self.OUTPUT_PATH: str = "result.TextGrid"

        BASE_DIR = Path(__file__).resolve().parents[2]

        self.AUDIO_FILE_PATH: Path = BASE_DIR / "records" / "SIZOYT_fixed.wav"
        self.DATABASE_FILE_PATH: Path = BASE_DIR / "data" / "LogopedData.db"
        self.JSON_FILE_PATH: Path = BASE_DIR / "data" / "TempData.json"
        
        self.private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
        self.public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
        self.algoritm: str = "RS256"
        
               
        self.COMPLETE_SCORE: int = 100
        self.ENOUGH_SCORE: int = 50
        self.MAX_ATTEMPTS: int = 3