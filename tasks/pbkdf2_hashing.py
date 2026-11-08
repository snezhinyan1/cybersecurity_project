# Проверка пароля с помощью PBKDF2-HMAC-SHA256. Случайная соль затрудняет повторное использование
# предварительно вычисленных результатов.

import hashlib
import secrets
import sys

# Число итераций задаётся одинаковым при создании и проверке производного ключа.
ITERATIONS = 100000


def generate_password_hash(password):
    # Для каждого сохранения пароля независимо генерируется 16-байтовая соль.
    salt = secrets.token_bytes(16)

    # Пароль кодируется в UTF-8 и передаётся PBKDF2 вместе с солью и числом итераций.
    derived_key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, ITERATIONS
    )

    # Соль и производный ключ сохраняются для последующей проверки.
    return salt, derived_key


def verify_password(stored_salt, stored_hash, input_password):
    # Производный ключ для предъявленного пароля вычисляется с ранее сохранённой солью.
    calculated_key = hashlib.pbkdf2_hmac(
        "sha256", input_password.encode("utf-8"), stored_salt, ITERATIONS
    )

    # Проверка сравнивает производные ключи без остановки на первом несовпадающем байте.
    return secrets.compare_digest(stored_hash, calculated_key)


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    user_password = "correct_horse_battery_staple"
    db_salt, db_hash = generate_password_hash(user_password)

    is_valid = verify_password(db_salt, db_hash, "correct_horse_battery_staple")
    print(f"Результат верификации корректного пароля: {is_valid}")
