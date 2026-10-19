#  Алгоритм консенсуса Proof-of-Work.
#  Реализация алгоритма доказательства выполнения работы. Метод требует выполнения
#  вычислительно сложной задачи поиска значения (nonce), при котором криптографический хэш
#  данных удовлетворяет заданному условию сложности.

import hashlib
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def mine_block(transactions, difficulty):
    print(f"Инициализация вычислений. Целевой префикс: {difficulty} нулевых битов.")

    # Формирование целевого префикса в соответствии с заданным параметром сложности.
    prefix = "0" * difficulty
    nonce = 0

    start_time = time.time()

    while True:
        # Конкатенация информационного блока транзакций и переменной nonce.
        data = f"{transactions}{nonce}".encode("utf-8")  # noqa: UP012
        # Вычисление хэш-функции SHA-256 от полученной строки.
        block_hash = hashlib.sha256(data).hexdigest()

        # Проверка соответствия вычисленного хэша целевому условию.
        if block_hash.startswith(prefix):
            time_taken = time.time() - start_time
            return nonce, block_hash, time_taken

        # Инкрементация переменной nonce в случае несоответствия условию.
        nonce += 1


nonce, b_hash, t = mine_block("Перевод Алиса->Боб: 10 BTC", difficulty=5)
print(f"Вычисления завершены. Значение nonce: {nonce}")
print(f"Результирующий хэш: {b_hash}")
print(f"Затраченное процессорное время: {t:.2f} сек.")
