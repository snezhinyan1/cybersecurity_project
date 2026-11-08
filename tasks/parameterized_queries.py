# Параметризованный поиск в SQLite. Имя пользователя передаётся отдельно от текста SQL-запроса.

import sqlite3
import sys


def find_user(connection, username):
    """Ищет пользователя в таблице users с уникальным полем username."""
    # Значение имени связывается с заполнителем ?. Кавычки внутри имени остаются частью данных.
    cursor = connection.execute(
        "SELECT id, username FROM users WHERE username = ?", (username,)
    )
    # Метод возвращает найденную строку либо None при отсутствии совпадений.
    return cursor.fetchone()


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Демонстрационная база создаётся в оперативной памяти.
    connection = sqlite3.connect(":memory:")
    try:
        # Уникальность имени обеспечивает не более одного результата поиска.
        connection.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE)"
        )
        # Имена добавляются как параметры, включая имя с апострофом.
        connection.executemany(
            "INSERT INTO users (username) VALUES (?)", [("alice",), ("O'Connor",)]
        )
        print("Обычное имя:", find_user(connection, "alice"))
        print("Имя с кавычкой:", find_user(connection, "O'Connor"))
        # Строка, похожая на часть SQL-условия, проверяется как буквальное имя.
        print("Попытка изменить условие запроса:", find_user(connection, "' OR 1=1 --"))
    finally:
        # Соединение закрывается и при успешном завершении, и при исключении.
        connection.close()
