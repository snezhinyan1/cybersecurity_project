#  Луковая маршрутизация.
#  Имитационная модель луковой маршрутизации. Алгоритм демонстрирует метод
#  инкапсуляции данных посредством многослойного шифрования для обеспечения анонимности
#  отправителя в сетях с распределенной архитектурой.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def onion_encrypt(message, node_keys):
    encrypted = message

    # Итерация по ключам узлов маршрута в обратном порядке для последовательной инкапсуляции.
    for key in reversed(node_keys):
        # Наложение слоя шифрования с использованием операции XOR.
        encrypted = bytes(
            a ^ b for a, b in zip(encrypted.encode(), key * len(encrypted))
        ).hex()
    return encrypted


def onion_decrypt(payload, node_keys):
    current_payload = payload

    # Итерация по узлам в прямом порядке для последовательной деинкапсуляции пакета.
    for i, key in enumerate(node_keys):
        raw_bytes = bytes.fromhex(current_payload)

        # Расшифрование текущего слоя соответствующим симметричным ключом узла.
        current_payload = bytes(
            a ^ b for a, b in zip(raw_bytes, key * len(raw_bytes))
        ).decode()

        print(
            f"Слой узла {i + 1} успешно удален. Промежуточные данные: {current_payload[:15]}..."
        )

    return current_payload


keys = [b"key1", b"key2", b"key3"]
onion = onion_encrypt("TOP SECRET DATA", keys)

print("Инкапсулированный пакет данных:", onion)
print("Результат маршрутизации и расшифрования:", onion_decrypt(onion, keys))
