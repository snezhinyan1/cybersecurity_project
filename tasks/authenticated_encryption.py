# Учебная схема Encrypt-then-MAC на основе XOR и HMAC-SHA256. Повторение XOR-ключа ослабляет
# конфиденциальность.

import hashlib
import hmac
import sys


def xor_with_key(data, key):
    # Непустой ключ необходим для циклического обращения к его байтам.
    if not key:
        raise ValueError("Ключ XOR не может быть пустым.")

    # Результат накапливается в изменяемом массиве байтов.
    result = bytearray()
    for index, byte in enumerate(data):
        # Остаток от деления индекса на длину ключа задаёт циклическую позицию в ключе.
        key_byte = key[index % len(key)]
        # XOR объединяет соответствующие биты байта данных и байта ключа.
        result.append(byte ^ key_byte)
    return bytes(result)


def authenticated_encrypt(plaintext, enc_key, mac_key):
    if not mac_key:
        raise ValueError("Ключ HMAC не может быть пустым.")
    # Кодирование в UTF-8 переводит исходный текст в байты для побитовой операции.
    ciphertext = xor_with_key(plaintext.encode("utf-8"), enc_key)

    # Метка вычисляется от шифротекста с отдельным ключом HMAC.
    mac = hmac.new(mac_key, ciphertext, hashlib.sha256).digest()

    return ciphertext, mac


def authenticated_decrypt(ciphertext, mac, enc_key, mac_key):
    if not mac_key:
        raise ValueError("Ключ HMAC не может быть пустым.")
    # Полученная метка проверяется относительно метки, заново вычисленной по шифротексту.
    expected_mac = hmac.new(mac_key, ciphertext, hashlib.sha256).digest()

    # Сравнение не прерывается при первом несовпадающем байте, что снижает риск утечки по времени.
    if not hmac.compare_digest(mac, expected_mac):
        raise ValueError("Ошибка верификации: нарушение целостности данных.")

    # Повторный XOR с тем же ключом восстанавливает байты исходного текста.
    return xor_with_key(ciphertext, enc_key).decode("utf-8")


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    encryption_key = b"k1"
    hmac_key = b"k2"
    ciphertext, tag = authenticated_encrypt("Привет!", encryption_key, hmac_key)
    recovered = authenticated_decrypt(ciphertext, tag, encryption_key, hmac_key)
    print("После расшифрования:", recovered)

    tampered_ciphertext = bytearray(ciphertext)
    # Инверсия младшего бита первого байта моделирует изменение шифротекста.
    tampered_ciphertext[0] ^= 1
    try:
        authenticated_decrypt(tampered_ciphertext, tag, encryption_key, hmac_key)
    except ValueError as error:
        print(f"Подмена обнаружена. {error}")
