#  Аутентифицированное шифрование (AEAD).
#  Реализация протокола аутентифицированного шифрования по схеме Encrypt-then-MAC.
#  Метод обеспечивает конфиденциальность данных и криптографическую гарантию их целостности,
#  предотвращая атаки на изменение зашифрованного сообщения.

import hashlib
import hmac
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def authenticated_encrypt(plaintext, enc_key, mac_key):
    # Выполнение операции побайтового сложения по модулю 2 (XOR) между текстом и ключом шифрования.
    ciphertext = bytes(
        a ^ b for a, b in zip(plaintext.encode(), enc_key * len(plaintext))
    )

    # Генерация имитовставки HMAC на основе полученного шифротекста для обеспечения целостности.
    mac = hmac.new(mac_key, ciphertext, hashlib.sha256).digest()

    return ciphertext, mac


def authenticated_decrypt(ciphertext, mac, enc_key, mac_key):
    # Вычисление эталонного значения HMAC для верификации входящего шифротекста.
    expected_mac = hmac.new(mac_key, ciphertext, hashlib.sha256).digest()

    # Безопасное сравнение хэшей за константное время для предотвращения атак по времени (timing attacks).
    if not hmac.compare_digest(mac, expected_mac):
        raise ValueError("Ошибка верификации: нарушение целостности данных.")

    # Декодирование сообщения при условии успешной верификации криптографической подписи.
    return bytes(a ^ b for a, b in zip(ciphertext, enc_key * len(ciphertext))).decode()


# Демонстрация работы алгоритма при отсутствии вмешательства.
c, m = authenticated_encrypt("Send $100", b"k1", b"k2")
print("Результат дешифрования:", authenticated_decrypt(c, m, b"k1", b"k2"))

# Моделирование преднамеренного искажения данных в канале связи.
hacked_c = bytearray(c)
hacked_c[0] ^= 0x01

try:
    # Попытка дешифрования поврежденного пакета данных.
    authenticated_decrypt(hacked_c, m, b"k1", b"k2")
except Exception as e:  # noqa: BLE001
    print(f"Исключение перехвачено: {e}")
