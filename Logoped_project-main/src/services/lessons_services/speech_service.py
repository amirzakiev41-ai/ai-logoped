from pathlib import Path
import re
import whisper

from core.exceptions import SpeechRecognitionError, WhisperModelError, AudioFileNotFoundError, WordSaveError


class SpeechService:
    def __init__(self, settings) -> None:
        self.settings = settings
        try:
            self.model = whisper.load_model(self.settings.MODEL)
        except Exception as e:
            raise WhisperModelError(f"Не удалось загрузить модель Whisper '{self.settings.MODEL}'.") from e

    def audio_to_text(self, audiofile_path: str | Path) -> str:
        try:
            transcribe = self.model.transcribe(
                str(audiofile_path),
                language="ru",
                task="transcribe"
            )

            text = transcribe["text"].lower().strip()
            text = re.sub(r"[^\w\s]", "", text)

            return text

        except FileNotFoundError as e:
            raise AudioFileNotFoundError("Аудиофайл не найден.") from e

        except Exception as e:
            raise SpeechRecognitionError(f"Ошибка распознавания речи: {e}") from e

    def word_to_file(self, word: str) -> None:
        try:
            with open("data/word.txt", "w", encoding="utf-8") as file:
                file.write(word)

        except OSError as e:
            raise WordSaveError("Не удалось сохранить слово.") from e