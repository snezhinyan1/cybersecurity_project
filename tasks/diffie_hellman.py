# Протокол Диффи-Хеллмана.
# Криптографический алгоритм безопасного обмена ключами.
# Демонстрирует математический принцип вычисления общего секрета
# двумя сторонами через незащищенный канал связи с использованием
# свойств возведения в степень в конечном поле.

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import secrets


def diffie_hellman_exchange():
    # Инициализация общедоступных параметров протокола.
    # Значения простого модуля и генератора передаются в открытом виде.
    p_modulus = 23
    g_base = 5

    # Генерация приватных ключей сторон, не подлежащих передаче по каналу связи.
    private_key_alice = secrets.randbelow(p_modulus - 2) + 2
    private_key_bob = secrets.randbelow(p_modulus - 2) + 2

    # Вычисление публичных ключей для обмена.
    public_key_alice = pow(g_base, private_key_alice, p_modulus)
    public_key_bob = pow(g_base, private_key_bob, p_modulus)

    # Вычисление общего секрета каждой стороной с использованием полученного чужого публичного ключа.
    # Коммутативность возведения в степень в конечном поле гарантирует идентичность результата.
    shared_secret_alice = pow(public_key_bob, private_key_alice, p_modulus)
    shared_secret_bob = pow(public_key_alice, private_key_bob, p_modulus)

    return shared_secret_alice, shared_secret_bob


secret_a, secret_b = diffie_hellman_exchange()

print(f"Вычисленный общий секрет стороны А: {secret_a}")
print(f"Вычисленный общий секрет стороны Б: {secret_b}")
