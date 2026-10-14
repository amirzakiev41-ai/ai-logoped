import sqlite3 as sq
from abc import  abstractmethod

from core.config import Settings
from core.exceptions import DatabaseConnectionError


class BaseRepository:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.database_path = self.settings.DATABASE_FILE_PATH
        self.create_table()
    
    @abstractmethod
    def create_table(self):
        pass

    def _connect(self) -> sq.Connection:
        try:
            return sq.connect(self.database_path)
        except sq.Error as e:
            raise DatabaseConnectionError(
                "Не удалось подключиться к базе данных."
            ) from e
    
    def _close_connection(self, db: sq.Connection | None) -> None:
        if db:
            db.close()
    
    def _rollback(self, db: sq.Connection | None) -> None:
        if db:
            db.rollback()