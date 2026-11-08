# Внедрение текста в младшие биты контейнера. Каждый байт контейнера хранит один бит сообщения.

import sys


def embed_message(container_bytes, message):
    # Байт 0xFF не встречается в корректном UTF-8 и заменяет нулевые байты текста.
    # Нулевой байт после текста служит маркером конца сообщения.
    msg_bytes = message.encode("utf-8").replace(b"\x00", b"\xff") + b"\x00"

    # Каждый байт представляется ровно восемью двоичными цифрами, включая ведущие нули.
    msg_bits = "".join(f"{byte:08b}" for byte in msg_bytes)

    # Число битов сообщения с маркером не должно превышать число байтов контейнера.
    if len(msg_bits) > len(container_bytes):
        raise ValueError("Размер контейнера недостаточен для внедрения сообщения.")

    # Контейнер копируется в изменяемый массив, чтобы сохранить исходные данные.
    stego_container = bytearray(container_bytes)

    # Маска 254 сбрасывает младший бит. Побитовое ИЛИ записывает на его место бит сообщения.
    for i, bit in enumerate(msg_bits):
        stego_container[i] = (stego_container[i] & 254) | int(bit)

    return stego_container


def extract_message(stego_container):
    message_bytes = bytearray()

    # Обрабатываются только полные группы из восьми байтов контейнера.
    for start in range(0, len(stego_container) - 7, 8):
        chunk = stego_container[start : start + 8]
        # Маска 1 выделяет младший бит каждого байта выбранной группы.
        bits = "".join(str(byte & 1) for byte in chunk)
        # Восемь выделенных битов восстанавливают один байт сообщения.
        message_byte = int(bits, 2)
        # При достижении маркера восстанавливаются внутренние нули и выполняется декодирование
        # UTF-8.
        if message_byte == 0:
            return message_bytes.replace(b"\xff", b"\x00").decode("utf-8")
        message_bytes.append(message_byte)

    # Отсутствие маркера конца означает, что извлечение завершилось некорректно.
    raise ValueError("В контейнере нет метки конца сообщения.")


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Имитация фрагмента данных цифрового изображения.
    dummy_image_data = bytearray(b"\xaa\xbb\xcc\xdd\xee\xff\x00\x11" * 10)
    secret_text = "Hidden"

    stego_data = embed_message(dummy_image_data, secret_text)
    recovered_text = extract_message(stego_data)

    print(f"Извлеченное скрытое сообщение: {recovered_text}")
