# Безопасное хранение паролей (PBKDF2).
# Реализация функции формирования ключа на основе пароля.
# Использование уникальной криптографической соли и большого числа
# итераций хэширования обеспечивает защиту базы данных от
# предварительно вычисленных таблиц и атак полным перебором.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import hashlib
import secrets


def generate_password_hash(password):
    # Генерация криптографически стойкой псевдослучайной последовательности (соли).
    # Использование уникальной соли предотвращает атаки с использованием радужных таблиц.
    salt = secrets.token_bytes(16)

    # Применение алгоритма PBKDF2 с HMAC-SHA256 и заданным количеством итераций.
    # Высокое число итераций экспоненциально увеличивает затраты вычислительных ресурсов при брутфорсе.
    iterations = 100000
    derived_key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations
    )

    return salt, derived_key


def verify_password(stored_salt, stored_hash, input_password):
    # Вычисление хэша вводимого пароля с использованием ранее сохраненной соли базы данных.
    iterations = 100000
    calculated_key = hashlib.pbkdf2_hmac(
        "sha256", input_password.encode("utf-8"), stored_salt, iterations
    )

    # Безопасное сравнение полученного ключа с эталонным значением из базы данных.
    return secrets.compare_digest(stored_hash, calculated_key)


user_password = "correct_horse_battery_staple"
db_salt, db_hash = generate_password_hash(user_password)

is_valid = verify_password(db_salt, db_hash, "correct_horse_battery_staple")
print(f"Результат верификации корректного пароля: {is_valid}")
