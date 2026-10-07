from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from core.config import Settings
from services.lessons_services.diagnostics_service import DiagnosticsService
from services.lessons_services.speech_service import SpeechService
from services.statistic_service import StatisticsService
from models.lesson_models import LessonResult, LessonWord
from models.statistics_models import SaveResultData


class LessonService:
    def __init__(
        self,
        settings: Settings,
        statistics_service: StatisticsService,
        speech_service: SpeechService,
        diagnostic_service: DiagnosticsService,
    ) -> None:
        self.settings = settings
        self.diagnostic = diagnostic_service
        self.recognition = speech_service
        self.statistics = statistics_service

    async def check_pronunciation(
        self,
        user_id: int,
        word_letter: LessonWord,
        audio: UploadFile,
    ) -> LessonResult:

        # Сохраняем загруженное аудио во временный файл
        suffix = Path(audio.filename or ".wav").suffix

        with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = Path(temp_file.name)

            content = await audio.read()
            temp_file.write(content)

        try:
            attempts = 1

            while attempts <= self.settings.MAX_ATTEMPTS:
                lesson_result = self._evaluate_word(
                    expected_word=word_letter.word,
                    audiofile_path=temp_path,
                )

                if self._check_status(
                    word_letter.word,
                    lesson_result.recognized_word,
                    lesson_result.status,
                ):
                    self._save_statistics(
                        user_id=user_id,
                        expected_word=word_letter.word,
                        lesson_result=lesson_result,
                        main_letter=word_letter.letter,
                    )

                    return lesson_result

                attempts += 1

            self._save_statistics(
                user_id=user_id,
                expected_word=word_letter.word,
                lesson_result=lesson_result,
                main_letter=word_letter.letter,
            )

            return lesson_result

        finally:
            # Удаляем временный файл после обработки
            temp_path.unlink(missing_ok=True)

    def _check_status(
        self,
        expected_word: str,
        recognized_word: str,
        status: str,
    ) -> bool:

        if status == "MISTAKE":
            print(
                self.diagnostic.analyze_errors(
                    expected_word,
                    recognized_word,
                )
            )
            return True

        elif status == "INVALID":
            return False

        elif status == "SUCCESS":
            return True

        return False

    def _evaluate_word(
        self,
        expected_word: str,
        audiofile_path: Path,
    ) -> LessonResult:

        recognized_word = self.recognition.audio_to_text(
            audiofile_path=audiofile_path
        )

        score_result = self.diagnostic.evaluate_score(
            expected_word=expected_word,
            recognized_text=recognized_word,
        )

        return LessonResult(
            recognized_word,
            score_result.status,
            score_result.score,
        )

    def _save_statistics(
        self,
        user_id: int,
        expected_word: str,
        lesson_result: LessonResult,
        main_letter: str,
    ) -> None:

        self.statistics.save_result(
            SaveResultData(
                user_id=user_id,
                expected_word=expected_word,
                main_letter=main_letter,
                lesson_result=lesson_result,
            )
        )