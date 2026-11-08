# Доказательство выполнения работы. Ограниченный перебор находит хэш SHA-256 с заданным числом
# начальных шестнадцатеричных нулей.

import hashlib
import sys
import time


def mine_block(transactions, difficulty, max_attempts=1_000_000):
    # Шестнадцатеричная запись SHA-256 содержит 64 цифры, что ограничивает длину префикса.
    if type(difficulty) is not int or not 0 <= difficulty <= 64:
        raise ValueError("Сложность должна быть целым числом от 0 до 64.")
    # Положительный предел попыток ограничивает объём перебора.
    if type(max_attempts) is not int or max_attempts < 1:
        raise ValueError("Число попыток должно быть положительным целым.")

    # Одна шестнадцатеричная цифра соответствует четырём битам.
    prefix = "0" * difficulty
    # Монотонный таймер используется для измерения продолжительности поиска.
    start_time = time.perf_counter()

    # Кандидаты проверяются по возрастанию от нуля до предела попыток.
    for nonce in range(max_attempts):
        # Разделитель отделяет сообщение от десятичной записи перебираемого числа.
        data = f"{transactions}:{nonce}".encode("utf-8")
        # Хэш входных байтов представляется в шестнадцатеричной форме.
        block_hash = hashlib.sha256(data).hexdigest()

        # Первый кандидат с требуемым префиксом завершает перебор.
        if block_hash.startswith(prefix):
            time_taken = time.perf_counter() - start_time
            return nonce, block_hash, time_taken

    # По исчерпании попыток сообщается, что подходящий хэш не найден.
    raise RuntimeError("Хэш не найден за указанное число попыток.")


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    difficulty = 3
    print(f"Ищем хэш с {difficulty} нулями в начале (в шестнадцатеричной записи).")
    nonce, block_hash, elapsed = mine_block("Перевод Алиса->Боб: 10 BTC", difficulty)
    print(f"Найденное число (nonce): {nonce}")
    print(f"Хэш SHA-256: {block_hash}")
    print(f"Время поиска: {elapsed:.4f} сек.")
