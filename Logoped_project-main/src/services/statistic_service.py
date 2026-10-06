from core.exceptions import UnsupportedLetterError, ResultNotFoundError
from core.constants import Constants
from database.result_repository import ResultRepository
from database.user_repisitory import UserRepository
from services.users_services.user_service import UserService
from models.statistics_models import StatisticsResult, SaveResultData, LetterStatisticsResult


class StatisticsService:
    def __init__(self, result_repository: ResultRepository, user_repository: UserRepository, user_service: UserService, constants: Constants):
        self.constants: Constants = constants
        self.result_repository: ResultRepository = result_repository
        self.user_repository: UserRepository = user_repository
        self.user_service: UserService = user_service
    
    def save_result(self, data: SaveResultData) -> None:
        self.result_repository.add_result(
            user_id=data.user_id,
            expected_word=data.expected_word,
            recognized_word=data.lesson_result.recognized_word,
            score=data.lesson_result.score,
            status=data.lesson_result.status,
            main_letter=data.main_letter,
        )

    def get_general_statistics(self, user_id: int) -> StatisticsResult:
        self.user_service._get_existing_user(user_id=user_id)
        
        attempts_count = self.result_repository.get_attempts_count(user_id=user_id)
        average_score = self.result_repository.get_average_score(user_id=user_id)
        success_count = self.result_repository.get_success_count(user_id=user_id)

        return StatisticsResult(
            attempts_count=attempts_count,
            average_score=average_score,
            success_count=success_count,
        )

    def get_statistics_by_letter(self, user_id: int, letter: str) -> LetterStatisticsResult:
        self.user_service._get_existing_user(user_id=user_id)
        self._check_supported_letter(letter=letter)
        
        attempts_count = self.result_repository.get_attempts_count_by_letter(user_id=user_id, letter=letter)
        average_score = self.result_repository.get_average_score_by_letter(user_id=user_id, letter=letter)
        success_count = self.result_repository.get_success_count_by_letter(user_id=user_id, letter=letter)

        return LetterStatisticsResult(
            letter=letter,
            attempts_count=attempts_count,
            average_score=average_score,
            success_count=success_count,
        )
    
    def get_all_statistics_of_letters(self, user_id: int,) -> list[LetterStatisticsResult]:
        self.user_service._get_existing_user(user_id=user_id)
        
        rows = self.result_repository.get_statistics_by_letters(user_id)

        return [
            LetterStatisticsResult(
                letter=row[0],
                attempts_count=row[1],
                average_score=row[2],
                success_count=row[3],
            )
            for row in rows
        ]
        
    
    def delete_user_statistics(self, user_id: int) -> None:
        self.user_service._get_existing_user(user_id=user_id)
        
        deleted = self.result_repository.delete_user_results(user_id=user_id)
        
        if deleted == 0:
            raise ResultNotFoundError("Результат не найден.")
    
    def delete_user_result(self, result_id: int) -> None:
        deleted = self.result_repository.delete_result(result_id=result_id)
        
        if deleted == 0:
            raise ResultNotFoundError("Результат не найден.")
    
    def _check_supported_letter(self, letter: str) -> None:
        if letter not in self.constants.SUPPORTED_LETTERS:
            raise UnsupportedLetterError(
                f"Буква '{letter}' не поддерживается."
            )