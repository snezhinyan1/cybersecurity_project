# Двухфакторная аутентификация (TOTP).
# Реализация алгоритма генерации одноразовых паролей на основе времени.
# Метод использует криптографическую функцию HMAC и разделяемый секрет
# для создания динамического токена авторизации ограниченного срока действия.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import hashlib
import hmac
import struct
import time


def generate_totp_code(secret_key, time_step=30):
    # Определение текущего временного интервала.
    # Стандартное окно валидности кода составляет 30 секунд.
    current_interval = int(time.time()) // time_step

    # Упаковка целочисленного значения интервала в 8-байтовый массив формата big-endian.
    interval_bytes = struct.pack(">Q", current_interval)

    # Вычисление HMAC-SHA1 от временного интервала с использованием разделяемого секрета.
    hmac_hash = hmac.new(secret_key, interval_bytes, hashlib.sha1).digest()

    # Определение динамического смещения (offset) на основе младших 4 бит последнего байта хэша.
    offset = hmac_hash[-1] & 0x0F

    # Извлечение 4-байтового фрагмента хэша по вычисленному смещению.
    # Наложение маски 0x7FFFFFFF отбрасывает старший бит во избежание проблем со знаком.
    truncated_hash = struct.unpack(">I", hmac_hash[offset : offset + 4])[0] & 0x7FFFFFFF

    # Формирование итогового 6-значного числового кода посредством операции деления по модулю.
    totp_code = truncated_hash % 1000000

    # Форматирование результата с ведущими нулями для обеспечения фиксированной длины кода.
    return f"{totp_code:06d}"


# Разделяемый секрет пользователя, хранящийся на сервере и в мобильном приложении.
user_secret = b"K7MJ52XJPI"
current_code = generate_totp_code(user_secret)

print(f"Сгенерированный токен авторизации (TOTP): {current_code}")
