# Обмен Диффи — Хеллмана на малых параметрах. Стороны вычисляют общий секрет по открытым значениям
# и собственным закрытым показателям. В примере стороны не аутентифицируют друг друга.

import sys

import secrets


def diffie_hellman_exchange():
    # Параметры общедоступны. Число 2 имеет порядок 11 по модулю 23.
    p_modulus = 23
    g_base = 2
    period = 11

    # Каждая сторона независимо выбирает ненулевой показатель в диапазоне от 1 до 10.
    private_key_alice = secrets.randbelow(period - 1) + 1
    private_key_bob = secrets.randbelow(period - 1) + 1

    # Открытые значения вычисляются возведением основания в соответствующую степень по модулю.
    public_key_alice = pow(g_base, private_key_alice, p_modulus)
    public_key_bob = pow(g_base, private_key_bob, p_modulus)

    # Обе стороны получают одну степень основания, поскольку произведения показателей a·b и b·a
    # равны.
    shared_secret_alice = pow(public_key_bob, private_key_alice, p_modulus)
    shared_secret_bob = pow(public_key_alice, private_key_bob, p_modulus)

    # Оба результата возвращаются для проверки совпадения в демонстрации.
    return shared_secret_alice, shared_secret_bob


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    secret_a, secret_b = diffie_hellman_exchange()

    print(f"Вычисленный общий секрет стороны А: {secret_a}")
    print(f"Вычисленный общий секрет стороны Б: {secret_b}")
