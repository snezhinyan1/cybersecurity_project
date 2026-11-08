# Учебная выборка LWE. Публичный вектор образуется прибавлением малых ошибок к произведению
# матрицы на секретный вектор. При выбранных параметрах секрет допускает перебор.

import random
import sys


def generate_postquantum_key(vector_size=4, mod=17):
    # Для формирования выборки требуется положительное число координат.
    if type(vector_size) is not int or vector_size < 1:
        raise ValueError("Размер вектора должен быть положительным целым числом.")
    # При модуле не меньше трёх ошибки −1, 0 и 1 имеют разные остатки.
    if type(mod) is not int or mod < 3:
        raise ValueError("Модуль должен быть целым числом не меньше трёх.")
    # Компоненты секретного вектора выбираются из множества остатков по модулю.
    secret_s = [random.randint(0, mod - 1) for _ in range(vector_size)]

    # Квадратная матрица задаёт коэффициенты учебной системы уравнений.
    matrix_a = [
        [random.randint(0, mod - 1) for _ in range(vector_size)]
        for _ in range(vector_size)
    ]

    # Каждой строке матрицы соответствует одна случайная ошибка из заданного набора.
    error_e = [random.choice([-1, 0, 1]) for _ in range(vector_size)]

    # Значения правой части вычисляются отдельно для каждой строки.
    public_b = []
    for row, error in zip(matrix_a, error_e):
        row_sum = 0
        for coefficient, secret_value in zip(row, secret_s):
            # Сумма попарных произведений образует скалярное произведение строки и секрета.
            row_sum += coefficient * secret_value
        # К точному значению прибавляется ошибка. Результат приводится по модулю.
        public_b.append((row_sum + error) % mod)

    # Матрица и вектор результатов публичны. Секретный вектор возвращается для проверки примера.
    return matrix_a, public_b, secret_s


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Два уравнения позволяют проверить вычисления вручную.
    A, b, s = generate_postquantum_key(vector_size=2)
    print("Открытый параметр (Матрица A):", A)
    print("Открытый параметр (Вектор b):", b)
    print("Приватный параметр (Вектор s):", s)
