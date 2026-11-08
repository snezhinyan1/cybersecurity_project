# Проверка подлинности и целостности документа посредством HMAC-SHA256 с общим секретным ключом.

"""Проверьте подлинность документа с помощью общего секретного ключа.

Вход — байты документа и непустой ключ. Создайте метку HMAC-SHA256, затем
проверьте её для исходного и изменённого документа. Проверка возвращает bool.
Обе стороны знают один ключ и могут создавать такие метки.
"""

import hashlib
import hmac
import secrets
import sys


def sign_document(document_bytes, key):
    # Учебная схема требует непустой общий ключ.
    if not key:
        raise ValueError("Ключ HMAC не может быть пустым.")
    # HMAC связывает содержимое документа с секретным ключом и возвращается в виде байтов.
    return hmac.new(key, document_bytes, hashlib.sha256).digest()


def verify_document(document_bytes, signature, key):
    # Для предъявленного документа вычисляется контрольная метка с тем же ключом.
    expected_signature = sign_document(document_bytes, key)
    # Метки сравниваются без остановки на первом несовпадающем байте.
    return hmac.compare_digest(signature, expected_signature)


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Для примера формируется случайный 32-байтовый ключ.
    key = secrets.token_bytes(32)
    document = "Передать 100 рублей.".encode("utf-8")
    signature = sign_document(document, key)
    print("Метка HMAC:", signature.hex())
    print("Исходный документ прошёл проверку:", verify_document(document, signature, key))

    # Изменённый документ проверяется относительно метки исходного документа.
    changed_document = "Передать 900 рублей.".encode("utf-8")
    print("Изменённый документ прошёл проверку:", verify_document(changed_document, signature, key))
