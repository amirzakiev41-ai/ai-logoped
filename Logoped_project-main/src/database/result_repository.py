import sqlite3 as sq

from core.exceptions import DatabaseInitializationError, DatabaseDeleteError, DatabaseReadError, DatabaseWriteError
from database.base_repository import BaseRepository


class ResultRepository(BaseRepository):
    def create_table(self) -> None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            db.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    expected_word TEXT,
                    recognized_word TEXT,
                    main_letter TEXT,
                    score INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            db.commit()

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseInitializationError(
                "Не удалось инициализировать базу данных."
            ) from e

        finally:
            self._close_connection(db)

    def add_result(
        self,
        user_id: int,
        expected_word: str,
        recognized_word: str,
        score: float,
        status: str,
        main_letter: str
    ) -> None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            db.execute("""
                INSERT INTO results (
                    user_id,
                    expected_word,
                    recognized_word,
                    main_letter,
                    score,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                expected_word,
                recognized_word,
                main_letter,
                score,
                status
            ))

            db.commit()

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseWriteError(
                "Не удалось сохранить результат.", str(e)
            ) from e

        finally:
            self._close_connection(db)

    def get_results(self) -> list[tuple]:
        db: sq.Connection | None = None
        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT *
                FROM results
                ORDER BY created_at DESC
            """)

            return cursor.fetchall()

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить результаты."
            ) from e

        finally:
            self._close_connection(db)

    def get_user_results(self, user_id: int) -> list[tuple]:
        db: sq.Connection | None = None
        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT *
                FROM results
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))

            return cursor.fetchall()

        except sq.Error as e:
            raise DatabaseReadError(
                f"Не удалось получить результаты пользователя '{user_id}'."
            ) from e

        finally:
            self._close_connection(db)
    
    def get_statistics_by_letters(self, user_id: int) -> list[tuple]:
        db: sq.Connection | None = None

        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT
                    main_letter,
                    COUNT(*) AS attempts_count,
                    AVG(score) AS average_score,
                    SUM(
                        CASE
                            WHEN status = 'SUCCESS' THEN 1
                            ELSE 0
                        END
                    ) AS success_count
                FROM results
                WHERE user_id = ?
                GROUP BY main_letter
                ORDER BY main_letter
            """, (user_id,))

            return cursor.fetchall()

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить статистику по буквам."
            ) from e

        finally:
            self._close_connection(db)

    def delete_user_results(self, user_id: int) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("""
                DELETE FROM results
                WHERE user_id = ?
            """, (user_id,))

            db.commit()
            
            return cursor.rowcount

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseDeleteError(
                "Не удалось удалить статистику пользователя."
            ) from e

        finally:
            self._close_connection(db)

    def delete_result(self, result_id: int) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("""
            DELETE FROM results
            WHERE id = ?
            """, (result_id,))

            db.commit()
            
            return cursor.rowcount

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseDeleteError(
                "Не удалось удалить результат."
            ) from e

        finally:
            self._close_connection(db)

    def clear_results(self) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            db.execute("BEGIN")

            cursor = db.execute("DELETE FROM results")

            db.commit()
            
            return cursor.rowcount

        except sq.Error as e:
            self._rollback(db)
            raise DatabaseDeleteError(
                "Не удалось очистить таблицу результатов."
            ) from e

        finally:
            self._close_connection(db)

    def get_attempts_count(self, user_id: int) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT COUNT(*)
                FROM results
                WHERE user_id = ?
            """, (user_id,))

            result = cursor.fetchone()
            return result[0] if result else 0

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить общее количество попыток."
            ) from e

        finally:
            self._close_connection(db)
    
    def get_attempts_count_by_letter(self, user_id: int, letter: str) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT COUNT(*)
                FROM results
                WHERE user_id = ?
                  AND main_letter = ?
            """, (user_id, letter,))

            result = cursor.fetchone()
            return result[0] if result else 0

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить общее количество попыток."
            ) from e

        finally:
            self._close_connection(db)

    def get_average_score(self, user_id: int) -> float | None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            cursor = db.execute("""
                SELECT AVG(score)
                FROM results
                WHERE user_id = ?
            """, (user_id,))

            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else None

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось вычислить средний балл."
            ) from e

        finally:
            self._close_connection(db)

    def get_success_count(self, user_id: int) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT COUNT(*)
                FROM results
                WHERE user_id = ?
                  AND status = 'SUCCESS'
            """, (user_id,))

            result = cursor.fetchone()
            return result[0] if result else 0

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить количество успешных попыток."
            ) from e

        finally:
            self._close_connection(db)
    
    def get_average_score_by_letter(self, user_id: int, letter: str) -> float | None:
        db: sq.Connection | None = None
        try:
            db = self._connect()
            cursor = db.execute("""
                SELECT AVG(score)
                FROM results
                WHERE user_id = ?
                  AND main_letter = ?
            """, (user_id, letter,))

            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else None

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось вычислить средний балл."
            ) from e

        finally:
            self._close_connection(db)

    def get_success_count_by_letter(self, user_id: int, letter: str) -> int:
        db: sq.Connection | None = None
        try:
            db = self._connect()

            cursor = db.execute("""
                SELECT COUNT(*)
                FROM results
                WHERE user_id = ?
                  AND main_letter = ?
                  AND status = 'SUCCESS'
            """, (user_id, letter,))

            result = cursor.fetchone()
            return result[0] if result else 0

        except sq.Error as e:
            raise DatabaseReadError(
                "Не удалось получить количество успешных попыток."
            ) from e

        finally:
            self._close_connection(db)