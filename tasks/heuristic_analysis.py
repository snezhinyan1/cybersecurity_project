#  Эвристический анализ на основе информационной энтропии.
#  Реализация базового эвристического анализатора. Алгоритм вычисляет
#  информационную энтропию Шеннона с использованием скользящего окна для выявления
#  участков файла с высокой плотностью данных, характерной для зашифрованного кода.

import math
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def chunk_entropy(chunk):
    # Подсчет частоты встречаемости каждого уникального байта в переданном блоке данных.
    freq = Counter(chunk)
    ent = 0.0

    for f in freq.values():
        # Вычисление вероятности появления байта и суммирование показателя энтропии Шеннона.
        p = f / len(chunk)
        ent -= p * math.log2(p)
    return ent


def scan_file_for_malware(data, window_size=16):
    print("Инициализация эвристического сканирования...")
    suspicions = []

    # Итерация по массиву данных с использованием скользящего окна. Смещение составляет 1 байт.
    for i in range(len(data) - window_size + 1):
        chunk = data[i : i + window_size]
        entropy = chunk_entropy(chunk)

        # Регистрация участков, значение энтропии которых превышает заданный порог аномальности.
        if entropy > 3.8:
            suspicions.append((i, round(entropy, 2)))

    return suspicions


# Подготовка массива данных, содержащего структурированный текст и фрагмент с высокой энтропией.
fake_file = (
    b"This is a normal text file full of standard english words. "
    + b"\x1a\x8f\x3b\x9a\xc4\x21\x78\xff\xee\xdd\xcc\xbb\xaa\x99\x88\x77"
)

print(
    "Зарегистрированы аномальные участки по следующим смещениям:",
    scan_file_for_malware(fake_file),
)
