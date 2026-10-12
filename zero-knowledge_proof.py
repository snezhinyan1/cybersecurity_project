#  Доказательство с нулевым разглашением (Протокол Шнорра).
#  Реализация интерактивного протокола, позволяющего доказывающей стороне (Prover)
#  подтвердить проверяющей стороне (Verifier) знание секрета без передачи самого секрета
#  или иной компрометирующей информации в канал связи.

import secrets
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def zkp_schnorr():
    # Инициализация параметров циклической группы, являющихся общедоступными.
    p = 23
    g = 5

    # Генерация открытого ключа на основе приватного секрета доказывающей стороны.
    password_secret_x = 6
    public_key_y = pow(g, password_secret_x, p)

    # Вычисление значения обязательства (Commitment) доказывающей стороной.
    k = secrets.randbelow(p - 1) + 1
    t = pow(g, k, p)

    # Генерация псевдослучайного вызова (Challenge) проверяющей стороной.
    c = secrets.randbelow(p - 1) + 1

    # Вычисление ответа (Response) доказывающей стороной с использованием секрета.
    s = (k + c * password_secret_x) % (p - 1)

    # Верификация корректности предоставленного ответа проверяющей стороной.
    left_side = pow(g, s, p)
    right_side = (t * pow(public_key_y, c, p)) % p

    print(f"Сравнение значений при верификации: {left_side} == {right_side}")

    return left_side == right_side


print("Статус завершения протокола верификации:", zkp_schnorr())
