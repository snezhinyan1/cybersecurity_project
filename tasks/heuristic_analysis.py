# Поиск участков с высокой энтропией Шеннона в последовательности байтов. Высокая энтропия сама по
# себе не устанавливает происхождение данных.

import math
import sys
from collections import Counter


def chunk_entropy(chunk):
    # Счётчик сопоставляет каждому встреченному байту число его появлений.
    freq = Counter(chunk)
    ent = 0.0

    for f in freq.values():
        # Относительная частота оценивает вероятность значения байта в окне.
        p = f / len(chunk)
        # Слагаемое −p·log₂(p) добавляется к энтропии в битах на байт.
        ent -= p * math.log2(p)
    return ent


def find_high_entropy_windows(data, window_size=16):
    # Проверяется допустимый размер скользящего окна.
    if type(window_size) is not int or window_size < 2:
        raise ValueError("Размер окна должен быть целым числом не меньше двух.")

    # Число возможных значений ограничено длиной окна и размером байтового алфавита.
    max_entropy = math.log2(min(window_size, 256))
    # Порог установлен на уровне 95 процентов от теоретической верхней границы.
    threshold = 0.95 * max_entropy
    windows = []

    # Последовательно рассматриваются все полные окна со сдвигом на один байт.
    for i in range(len(data) - window_size + 1):
        chunk = data[i : i + window_size]
        entropy = chunk_entropy(chunk)

        # Порог применяется к исходной величине. Округление используется только для представления
        # результата.
        if entropy > threshold:
            windows.append((i, round(entropy, 2)))

    return windows


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Образец объединяет обычный текст и участок с разнообразными значениями байтов.
    fake_file = (
        b"This is a normal text file full of standard english words. "
        + b"\x1a\x8f\x3b\x9a\xc4\x21\x78\xff\xee\xdd\xcc\xbb\xaa\x99\x88\x77"
    )

    print(
        "Окна с высокой энтропией (смещение, энтропия):",
        find_high_entropy_windows(fake_file),
    )
