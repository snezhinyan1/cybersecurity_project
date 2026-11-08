# Код Хэмминга (7,4). Три проверочных бита позволяют исправить одну ошибку в семибитовом кодовом
# слове.

import sys


def hamming_74_encode(data_bits):
    # Кодирование определено для четырёх двоичных информационных разрядов.
    if len(data_bits) != 4 or any(type(bit) is not int or bit not in (0, 1) for bit in data_bits):
        raise ValueError("Нужны четыре бита, каждый равен 0 или 1.")
    # Четыре входных значения сопоставляются информационным позициям.
    d1, d2, d3, d4 = data_bits

    # Каждый проверочный бит задаёт чётную сумму в своей группе позиций.
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    # Проверочные биты занимают позиции 1, 2 и 4 при нумерации с единицы.
    return [p1, p2, d1, p3, d2, d3, d4]


def hamming_74_decode_and_fix(encoded_bits):
    # Декодирование требует полного семибитового слова.
    if len(encoded_bits) != 7 or any(type(bit) is not int or bit not in (0, 1) for bit in encoded_bits):
        raise ValueError("Нужны семь битов, каждый равен 0 или 1.")
    # Неизменяемая последовательность копируется в список, чтобы можно было исправить разряд.
    if isinstance(encoded_bits, (tuple, bytes)):
        encoded_bits = list(encoded_bits)
    # Извлечение всех переданных битов из кодового слова.
    p1, p2, d1, p3, d2, d3, d4 = encoded_bits

    # Проверки чётности формируют три разряда синдрома.
    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s3 = p3 ^ d2 ^ d3 ^ d4

    # Ненулевой синдром задаёт номер позиции ошибки при предположении об одном искажении.
    error_pos = s1 * 1 + s2 * 2 + s3 * 4

    if error_pos > 0:
        print(f"Зарегистрировано искажение в бите {error_pos}. Производится коррекция.")
        # Инверсия разряда исправляет одиночную ошибку. Индекс списка на единицу меньше позиции.
        encoded_bits[error_pos - 1] ^= 1

    # Из исправленного слова извлекаются только информационные разряды.
    return [encoded_bits[2], encoded_bits[4], encoded_bits[5], encoded_bits[6]]


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    original = [1, 0, 1, 1]
    encoded = hamming_74_encode(original)

    # Присваивание нуля последнему разряду моделирует одиночное искажение в выбранном примере.
    encoded[6] = 0
    print("Восстановленная последовательность:", hamming_74_decode_and_fix(encoded))
