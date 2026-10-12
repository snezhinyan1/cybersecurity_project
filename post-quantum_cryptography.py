#  Постквантовая криптография (LWE).
#  Демонстрация базовых принципов криптографии на основе задачи обучения
#  с ошибками (Learning With Errors). Внесение малой псевдослучайной погрешности в систему
#  уравнений делает её вычислительно сложной для классических и квантовых алгоритмов.

import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def generate_postquantum_key(vector_size=4, mod=17):
    # Генерация секретного вектора, являющегося решением системы уравнений.
    secret_s = [random.randint(0, mod - 1) for _ in range(vector_size)]

    # Генерация публичной матрицы коэффициентов системы уравнений.
    matrix_a = [
        [random.randint(0, mod - 1) for _ in range(vector_size)]
        for _ in range(vector_size)
    ]

    # Формирование вектора псевдослучайных ошибок для внесения погрешности в расчеты.
    error_e = [random.choice([-1, 0, 1]) for _ in range(vector_size)]

    # Вычисление значений публичного вектора с добавлением сгенерированной погрешности.
    public_b = []
    for i in range(vector_size):
        row_sum = sum(matrix_a[i][j] * secret_s[j] for j in range(vector_size))
        public_b.append((row_sum + error_e[i]) % mod)

    # Возврат параметров открытого ключа (A, b) и приватного ключа (s).
    return matrix_a, public_b, secret_s


A, b, s = generate_postquantum_key()
print("Открытый параметр (Матрица A):", A)
print("Открытый параметр (Вектор b):", b)
print("Приватный параметр (Вектор s):", s)
