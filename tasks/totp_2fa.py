# Генерация шестизначного TOTP-кода.
# Номер временного интервала служит счётчиком для HMAC-SHA1.

import sys

import hashlib
import hmac
import struct
import time


def generate_totp_code(secret_key, time_step=30):
    # Участники должны располагать одним и тем же непустым секретом.
    if not secret_key:
        raise ValueError("Секрет TOTP не может быть пустым.")
    # Целочисленная длительность интервала должна быть больше нуля.
    if type(time_step) is not int or time_step < 1:
        raise ValueError("Длительность интервала должна быть положительным целым числом.")
    # Деление времени Unix на шаг с округлением вниз даёт номер текущего интервала.
    current_interval = int(time.time()) // time_step

    # Счётчик кодируется восемью байтами без знака в порядке от старшего к младшему.
    interval_bytes = struct.pack(">Q", current_interval)

    # Метка HMAC-SHA1 вычисляется от двоичного счётчика с общим секретом.
    hmac_hash = hmac.new(secret_key, interval_bytes, hashlib.sha1).digest()

    # Младшие четыре бита последнего байта метки задают смещение для динамического усечения.
    offset = hmac_hash[-1] & 0x0F

    # Четыре байта считываются по смещению. Маска очищает старший бит, оставляя 31-битовое число.
    truncated_hash = struct.unpack(">I", hmac_hash[offset : offset + 4])[0] & 0x7FFFFFFF

    # Остаток по модулю миллиона ограничивает числовое значение шестью десятичными разрядами.
    totp_code = truncated_hash % 1000000

    # Форматирование сохраняет ведущие нули и фиксированную длину кода.
    return f"{totp_code:06d}"


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # В демонстрации общий секрет задан как фиксированная последовательность байтов.
    user_secret = b"K7MJ52XJPI"
    current_code = generate_totp_code(user_secret)

    print(f"Сгенерированный токен авторизации (TOTP): {current_code}")
