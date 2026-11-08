# Учебная модель CBC. Сцепление блоков воспроизводится, а операция блочного шифрования заменена
# XOR с ключом. Линейность XOR допускает повторение выходных блоков.

import secrets
import sys


def xor_byte_arrays(b1, b2):
    # Проверка длин исключает молчаливое усечение при попарном обходе через zip.
    if len(b1) != len(b2):
        raise ValueError("Для XOR нужны массивы одинаковой длины.")
    # XOR применяется к каждой паре байтов с одинаковым индексом.
    return bytes(x ^ y for x, y in zip(b1, b2))


def cbc_encrypt_mock(plaintext_bytes, key_bytes, iv_bytes):
    # В этой модели длина ключа определяет размер блока.
    block_size = len(key_bytes)
    # Начальный вектор должен иметь размер блока, а размер блока должен быть положительным.
    if not block_size or len(iv_bytes) != block_size:
        raise ValueError("Ключ и начальный блок IV должны иметь одинаковую ненулевую длину.")

    # Маркер 0x80 отделяет исходные данные от дополняющих нулей.
    padded_text = plaintext_bytes + b"\x80"
    # Остаток показывает, сколько позиций уже занято в последнем неполном блоке.
    used_bytes = len(padded_text) % block_size
    # Нулевые байты добавляются до ближайшей границы блока.
    if used_bytes:
        padded_text += bytes(block_size - used_bytes)

    ciphertext = bytearray()
    # Для первого блока роль предыдущего шифроблока выполняет IV.
    previous_block = iv_bytes

    # Шаг цикла равен длине одного блока.
    for i in range(0, len(padded_text), block_size):
        block = padded_text[i : i + block_size]
        # Открытый блок объединяется с предыдущим шифроблоком посредством XOR.
        mixed_block = xor_byte_arrays(block, previous_block)
        # XOR с ключом имитирует преобразование блока.
        encrypted_block = xor_byte_arrays(mixed_block, key_bytes)
        ciphertext.extend(encrypted_block)
        # Текущий результат становится входом сцепления для следующего блока.
        previous_block = encrypted_block

    return bytes(ciphertext)


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Для демонстрации задаётся восьмибайтовый ключ и формируется IV той же длины.
    secret_key = b"KEY_1234"
    initialization_vector = secrets.token_bytes(len(secret_key))

    # Одинаковые блоки позволяют наблюдать повторения на выходе учебной модели.
    plaintext = b"BLOCK_A BLOCK_A BLOCK_A "
    encrypted_data = cbc_encrypt_mock(plaintext, secret_key, initialization_vector)

    print(f"Длина исходного текста: {len(plaintext)} байт")
    print("Блоки после XOR-сцепления:")
    for start in range(0, len(encrypted_data), len(secret_key)):
        block = encrypted_data[start : start + len(secret_key)]
        print(block.hex())
