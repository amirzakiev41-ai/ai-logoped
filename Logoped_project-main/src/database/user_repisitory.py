import sqlite3 as sq

from core.exceptions import *
from database.base_repository import BaseRepository
from models.user_models import UserModel


class UserRepository(BaseRepository):
    def create_table(self) -> None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            db.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE, 
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )"""
            )

            db.commit()

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseInitializationError(
                "Не удалось инициализировать базу данных.",
                str(e)
            ) from e

        finally:
            self._close_connection(db)
    
    def register_user(self, user_name: str, email: str) -> UserModel:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("""
                INSERT INTO users (user_name, email)
                VALUES (?, ?)
            """, (user_name, email))

            db.commit()

            return UserModel(
                    user_id=cursor.lastrowid,
                    user_name=user_name,
                    email=email,
                   )

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseWriteError(
                "Не удалось создать пользователя.", str(e)
            ) from e

        finally:
            self._close_connection(db)
    
    def create_user(self, user_name: str, email: str) -> UserModel:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("""
                INSERT INTO users (user_name, email)
                VALUES (?, ?)
            """, (user_name, email))

            db.commit()

            return UserModel(
                    user_id=cursor.lastrowid,
                    user_name=user_name,
                    email=email,
                   )

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseWriteError(
                "Не удалось создать пользователя.", str(e)
            ) from e

        finally:
            self._close_connection(db)
        
    def get_user_by_id(self, user_id: int) -> UserModel | None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.row_factory = sq.Row

            cursor = db.execute("""
                SELECT *
                FROM users
                WHERE user_id = ?
            """, (user_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return UserModel(
                user_id=row["user_id"],
                user_name=row["user_name"],
                email=row["email"],
            )

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить пользователя."
            ) from e

        finally:
            self._close_connection(db)
        
    def get_user_by_email(
        self, email: str) -> UserModel | None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.row_factory = sq.Row

            cursor = db.execute("""
                SELECT *
                FROM users
                WHERE email = ?
            """, (email,))

            row = cursor.fetchone()

            if row is None:
                return None

            return UserModel(
                user_id=row["user_id"],
                user_name=row["user_name"],
                email=row["email"],
            )

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить пользователя."
            ) from e

        finally:
            self._close_connection(db) 
    
    def get_all_users(self) -> list[UserModel]:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.row_factory = sq.Row

            cursor = db.execute("""
                SELECT *
                FROM users
                ORDER BY user_id
            """)

            rows = cursor.fetchall()

            return [
                UserModel(
                user_id=row["user_id"],
                user_name=row["user_name"],
                email=row["email"],
                )
                for row in rows
            ]

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить список пользователей."
            ) from e

        finally:
            self._close_connection(db)

    def update_user_name(
        self,
        user_id: int,
        user_name: str,
    ) -> int:

        db: sq.Connection | None = None

        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("""
                UPDATE users
                SET user_name = ?
                WHERE user_id = ?
            """, (
                user_name,
                user_id,
            ))

            db.commit()

            return cursor.rowcount

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseWriteError(
                "Не удалось изменить имя пользователя."
            ) from e

        finally:
            self._close_connection(db)

    def delete_user(self, user_id: int) -> int:
        db: sq.Connection | None = None

        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("""
                DELETE
                FROM users
                WHERE user_id = ?
            """, (user_id,))

            db.commit()

            return cursor.rowcount

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseDeleteError(
                "Не удалось удалить пользователя."
            ) from e

        finally:
            self._close_connection(db)