# Учебная модель последовательного наложения и снятия слоёв при луковой маршрутизации. XOR служит
# имитацией преобразования данных.

import sys

# Выбор формы импорта учитывает запуск скрипта и запуск в составе пакета.
if __package__:
    from .authenticated_encryption import xor_with_key
else:
    from authenticated_encryption import xor_with_key


def onion_encrypt(message, node_keys):
    # Входом первого преобразования служит исходное сообщение.
    encrypted = message

    # Ключ первого узла используется последним, чтобы его слой оказался внешним.
    for key in reversed(node_keys):
        # Байты каждого слоя представляются шестнадцатеричной строкой для следующего
        # преобразования.
        encrypted = xor_with_key(encrypted.encode("utf-8"), key).hex()
    return encrypted


def onion_decrypt(payload, node_keys):
    current_payload = payload

    # Узлы снимают слои в порядке прохождения маршрута, начиная с внешнего.
    for node, key in enumerate(node_keys, start=1):
        # Шестнадцатеричное представление текущего слоя преобразуется обратно в байты.
        raw_bytes = bytes.fromhex(current_payload)
        # Повторное применение XOR с ключом узла восстанавливает текст предыдущего слоя.
        current_payload = xor_with_key(raw_bytes, key).decode("utf-8")
        print(f"Узел {node} снял свой слой. Начало данных: {current_payload[:15]}")

    # После обработки последнего ключа возвращается исходное сообщение.
    return current_payload


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    keys = [b"key1", b"key2", b"key3"]
    onion = onion_encrypt("Привет", keys)
    print("Пакет со всеми слоями:", onion)
    print("Сообщение после снятия всех слоёв:", onion_decrypt(onion, keys))
