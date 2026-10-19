# Режим сцепления блоков шифротекста (CBC).
# Имитационная модель блочного шифрования. Алгоритм демонстрирует
# устранение статистических паттернов исходного сообщения путем
# применения операции XOR между текущим блоком открытого текста
# и предыдущим блоком шифротекста перед инкапсуляцией.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import secrets


def xor_byte_arrays(b1, b2):
    # Вспомогательная функция для побайтового сложения по модулю 2.
    return bytes(x ^ y for x, y in zip(b1, b2))


def cbc_encrypt_mock(plaintext_bytes, key_bytes, iv_bytes):
    # Инициализация массива для хранения результирующего шифротекста.
    ciphertext = bytearray()

    # Установка вектора инициализации в качестве предыдущего блока для первой итерации.
    previous_block = iv_bytes
    block_size = len(key_bytes)

    # Последовательная обработка фрагментов открытого текста фиксированной длины.
    for i in range(0, len(plaintext_bytes), block_size):
        block = plaintext_bytes[i : i + block_size]

        # Дополнение последнего блока нулевыми байтами при несоответствии длины.
        if len(block) < block_size:
            block += bytes(block_size - len(block))

        # Реализация схемы CBC: сложение текущего блока текста с предыдущим блоком шифротекста.
        # Данный шаг устраняет статистические паттерны исходного сообщения.
        mixed_block = xor_byte_arrays(block, previous_block)

        # Применение ключа шифрования к смешанному блоку.
        encrypted_block = xor_byte_arrays(mixed_block, key_bytes)

        ciphertext.extend(encrypted_block)

        # Сохранение текущего зашифрованного блока для использования в следующей итерации.
        previous_block = encrypted_block

    return bytes(ciphertext)


# Инициализация параметров блочного шифра с длиной блока 8 байт.
secret_key = b"KEY_1234"
initialization_vector = secrets.token_bytes(8)

# Использование текста с повторяющимися паттернами для демонстрации свойств CBC.
plaintext = b"BLOCK_A BLOCK_A BLOCK_A "
encrypted_data = cbc_encrypt_mock(plaintext, secret_key, initialization_vector)

print(f"Длина исходного текста: {len(plaintext)} байт")
print(f"Результат инкапсуляции CBC (hex): {encrypted_data.hex()}")
