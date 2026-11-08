# Контроль целостности файла по SHA-256. Изменение определяется сравнением с доверенным эталонным
# хэшем.

"""Обнаружьте изменение документа с помощью SHA-256.

Вход функции — путь к файлу. Результат — его хэш в шестнадцатеричной записи.
Сохраните исходный хэш, измените файл и сравните результаты.
Эталонный хэш должен храниться в доверенном месте.
"""

import hashlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


def file_sha256(path):
    # Объект SHA-256 хранит промежуточное состояние вычисления.
    digest = hashlib.sha256()
    # Двоичный режим передаёт алгоритму исходные байты файла.
    with open(path, "rb") as document:
        while True:
            # Чтение порциями по 64 КиБ ограничивает объём данных, одновременно загруженных в
            # память.
            chunk = document.read(65536)
            # Пустая порция означает достижение конца файла.
            if not chunk:
                break
            # Каждая прочитанная порция включается в общий хэш в порядке чтения.
            digest.update(chunk)
    # Результат представляется строкой из 64 шестнадцатеричных цифр.
    return digest.hexdigest()


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Демонстрационные файлы создаются во временной папке с автоматической очисткой.
    with TemporaryDirectory() as directory:
        path = Path(directory) / "document.txt"
        path.write_text("Сумма перевода — 100 рублей.", encoding="utf-8")
        original_hash = file_sha256(path)
        print("Исходный SHA-256:", original_hash)

        path.write_text("Сумма перевода — 900 рублей.", encoding="utf-8")
        # Повторное вычисление после изменения файла позволяет сравнить хэши двух версий.
        changed_hash = file_sha256(path)
        print("SHA-256 после изменения:", changed_hash)
        print("Документ изменён:", original_hash != changed_hash)
