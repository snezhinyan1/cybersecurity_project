# Стеганография на основе метода LSB.
# Алгоритм демонстрирует процесс скрытия текстовой информации внутри
# массива байтов (имитация цифрового изображения) посредством
# модификации наименьшего значащего бита каждого байта контейнера.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def embed_message(container_bytes, message):
    # Преобразование строкового сообщения в массив байтов кодировки utf-8.
    msg_bytes = message.encode("utf-8")

    # Формирование битовой последовательности исходного сообщения.
    msg_bits = "".join(f"{byte:08b}" for byte in msg_bytes)

    # Добавление нулевого байта в качестве маркера конца сообщения.
    msg_bits += "00000000"

    if len(msg_bits) > len(container_bytes):
        raise ValueError("Размер контейнера недостаточен для внедрения сообщения.")

    stego_container = bytearray(container_bytes)

    # Последовательная замена наименьшего значащего бита (LSB) каждого байта контейнера.
    # Операция побитового И с маской 254 (11111110) обнуляет последний бит.
    # Операция побитового ИЛИ устанавливает значение бита сообщения.
    for i, bit in enumerate(msg_bits):
        stego_container[i] = (stego_container[i] & 254) | int(bit)

    return stego_container


def extract_message(stego_container):
    extracted_bits = []

    # Извлечение наименьших значащих битов из контейнера.
    # Операция побитового И с маской 1 выделяет значение LSB.
    for byte in stego_container:
        extracted_bits.append(str(byte & 1))

    extracted_bits_str = "".join(extracted_bits)
    message_bytes = bytearray()

    # Группировка извлеченных битов по 8 для формирования байтов сообщения.
    for i in range(0, len(extracted_bits_str), 8):
        byte_str = extracted_bits_str[i : i + 8]
        if byte_str == "00000000":
            break
        message_bytes.append(int(byte_str, 2))

    return message_bytes.decode("utf-8")


# Имитация фрагмента данных цифрового изображения.
dummy_image_data = bytearray(b"\xaa\xbb\xcc\xdd\xee\xff\x00\x11" * 10)
secret_text = "Hidden"

stego_data = embed_message(dummy_image_data, secret_text)
recovered_text = extract_message(stego_data)

print(f"Извлеченное скрытое сообщение: {recovered_text}")
