# Восстановление секрета по долям Шамира. Значение многочлена при x = 0 вычисляется интерполяцией
# Лагранжа.

import math
import sys


def reconstruct_secret(shares, prime_mod):
    """Восстанавливает секрет по достаточному числу долей при простом модуле."""
    # Интерполяция требует непустого набора долей и допустимого модуля.
    if type(prime_mod) is not int or prime_mod < 2 or not shares:
        raise ValueError("Нужны доли и простой модуль.")
    # Простой модуль обеспечивает существование обратного элемента для любого ненулевого остатка.
    if any(prime_mod % divisor == 0 for divisor in range(2, math.isqrt(prime_mod) + 1)):
        raise ValueError("Модуль должен быть простым числом.")

    # Координаты сравниваются по остаткам, поскольку разные целые числа могут обозначать один
    # элемент поля.
    x_values = {x % prime_mod for x, _ in shares}
    # Нулевая координата раскрывает секрет, а совпадающие координаты обращают знаменатель в ноль.
    if 0 in x_values or len(x_values) != len(shares):
        raise ValueError("Координаты x долей должны быть ненулевыми и различными по модулю.")

    # В аккумуляторе суммируются вклады отдельных долей.
    secret = 0

    # Каждая доля добавляет к ответу свой вклад.
    for x, y in shares:
        numerator = 1
        denominator = 1

        # Вес доли строится по всем остальным координатам.
        for other_x, _ in shares:
            if other_x != x:
                # При подстановке x = 0 множитель числителя равен отрицанию координаты другой
                # доли.
                numerator = (numerator * -other_x) % prime_mod
                # Множитель знаменателя равен разности координат текущей и другой долей.
                denominator = (denominator * (x - other_x)) % prime_mod

        # Обратный элемент вычисляется возведением знаменателя в степень p − 2.
        inverse = pow(denominator, prime_mod - 2, prime_mod)
        # Значение доли умножается на её интерполяционный вес и прибавляется к результату по
        # модулю.
        secret = (secret + y * numerator * inverse) % prime_mod

    return secret


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Три точки многочлена y = 42 + 3x + 4x². Ожидаемый секрет при x = 0 равен 42.
    shares = [(1, 49), (2, 64), (3, 87)]
    print("Доли:", shares)
    print("Восстановленный секрет:", reconstruct_secret(shares, 257))
