from core.config import Settings
from core.constants import Constants
from services.lessons_services.lesson_service import LessonService
from services.statistic_service import StatisticsService
from services.lessons_services.word_service import WordService
from services.lessons_services.diagnostics_service import DiagnosticsService
from services.lessons_services.speech_service import SpeechService
from services.users_services.user_service import UserService
from database.result_repository import ResultRepository
from database.user_repisitory import UserRepository


class AppContainer:
    def __init__(self) -> None:
        self.settings: Settings = Settings()
        self.constants: Constants = Constants()

        self.result_repository: ResultRepository = ResultRepository(settings=self.settings)
        self.user_repository: UserRepository = UserRepository(settings=self.settings)

        self.user_service: UserService = UserService(repository=self.user_repository)
        self.statistics_service: StatisticsService = StatisticsService(
            constants=self.constants,
            result_repository=self.result_repository,
            user_repository=self.user_repository,
            user_service=self.user_service
        )
        
        self.diagnostic_service: DiagnosticsService = DiagnosticsService(settings=self.settings)
        self.speech_service: SpeechService = SpeechService(settings=self.settings)

        self.lesson_service: LessonService = LessonService(
            settings=self.settings,
            statistics_service=self.statistics_service,
            diagnostic_service=self.diagnostic_service,
            speech_service=self.speech_service
        )

        self.word_service: WordService = WordService(settings=self.settings)
