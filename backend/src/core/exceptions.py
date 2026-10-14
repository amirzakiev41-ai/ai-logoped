class WordNotFoundError(LookupError):
    """Слово не найдено."""

class UserNotFoundError(LookupError):
    """Пользователь не найден."""

class ResultNotFoundError(LookupError):
    """Результат не найден."""

class AudioFileNotFoundError(FileNotFoundError):
    """Аудиофайл не найден."""

class WhisperModelError(RuntimeError):
    """Ошибка загрузки Whisper."""

class SpeechRecognitionError(RuntimeError):
    """Ошибка распознавания речи."""

class WordSaveError(OSError):
    """Не удалось сохранить слово."""

class DatabaseConnectionError(ConnectionError):
    """Ошибка подключения к базе."""

class DatabaseReadError(RuntimeError):
    """Ошибка чтения базы данных."""

class DatabaseWriteError(RuntimeError):
    """Ошибка записи базы данных."""

class DatabaseDeleteError(RuntimeError):
    """Ошибка удаления из базы данных."""
    
class InvalidUserDataError(ValueError):
    """Ошибка данных пользователя"""

class InvalidPasswordError(PermissionError):
   """Ошибка пороля"""

class DatabaseInitializationError(RuntimeError):
    """Ошибка инициализации данных"""

class UnsupportedLetterError(ValueError):
    """Буква не поддерживается системой."""
    
class EmailAlreadyExistsError(ValueError):
    """Пользователь с такой почтой уже существует."""