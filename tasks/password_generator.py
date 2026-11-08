# Формирование случайного пароля заданной длины с обязательным представителем каждой из четырёх
# групп символов.

"""Создайте случайный пароль заданной длины.

Вход — целая длина от 4. Результат — пароль с латинскими буквами обоих регистров,
цифрой и специальным символом. Для демонстрации используется длина 16.
"""

import secrets
import string
import sys


# Константа ограничивает набор допустимых специальных символов.
SPECIAL_CHARACTERS = "!@#$%^&*"


def generate_password(length=16):
    # Для представления четырёх групп необходимы как минимум четыре позиции.
    if type(length) is not int or length < 4:
        raise ValueError("Длина должна быть целым числом не меньше 4.")

    # Латинские буквы разделяются по регистру. Цифры и специальные символы образуют отдельные
    # группы.
    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits, SPECIAL_CHARACTERS]
    characters = []
    # Из каждой группы выбирается один символ с использованием модуля secrets.
    for group in groups:
        characters.append(secrets.choice(group))

    # Объединённый алфавит используется для заполнения оставшихся позиций.
    alphabet = "".join(groups)
    # Число дополнительных выборок равно разности между требуемой длиной и числом обязательных
    # символов.
    for _ in range(length - len(groups)):
        characters.append(secrets.choice(alphabet))

    # Порядок символов перемешивается, чтобы обязательные позиции не были предсказуемы.
    secrets.SystemRandom().shuffle(characters)
    # Список символов объединяется в строку без разделителей.
    return "".join(characters)


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    password = generate_password(16)
    print("Случайный учебный пароль:", password)
    print("Количество символов:", len(password))
