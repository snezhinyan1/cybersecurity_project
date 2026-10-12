#  Разделение секрета Шамира.
#  Реализация криптографического протокола разделения секрета. Восстановление
#  исходного значения осуществляется посредством полиномиальной интерполяции Лагранжа
#  в конечном поле, вычисляющей свободный член полинома.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def reconstruct_secret(shares, prime_mod):
    secret = 0

    # Выполнение интерполяции Лагранжа для вычисления значения полинома в точке x = 0.
    for i, (x_i, y_i) in enumerate(shares):
        numerator = 1
        denominator = 1

        # Формирование базисных полиномов с использованием координат остальных долей.
        for j, (x_j, y_j) in enumerate(shares):
            if i != j:
                numerator = (numerator * (0 - x_j)) % prime_mod
                denominator = (denominator * (x_i - x_j)) % prime_mod

        # Нахождение мультипликативно обратного элемента знаменателя по Малой теореме Ферма.
        inv = pow(denominator, prime_mod - 2, prime_mod)

        # Суммирование вычисленного базисного значения в переменную восстанавливаемого секрета.
        secret = (secret + y_i * numerator * inv) % prime_mod

    return secret


# Инициализация массива долей, предоставленных участниками протокола.
keys = [(1, 149), (3, 203), (5, 117)]

print("Результат реконструкции секрета:", reconstruct_secret(keys, 257))
