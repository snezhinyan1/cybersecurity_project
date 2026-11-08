# Проверка соответствия пароля заданному набору учебных правил. Результат содержит все выявленные
# нарушения.

"""Проверьте пароль по заданным учебным правилам.

Вход — строка пароля и минимальная длина. Результат — список нарушенных правил.
Пароль должен содержать латинские буквы обоих регистров, цифру и символ из !@#$%^&*.
Выполнение этих правил само по себе не гарантирует стойкость пароля.
"""

import string
import sys


SPECIAL_CHARACTERS = "!@#$%^&*"


def check_password_rules(password, min_length=12):
    # Минимальная длина должна быть задана положительным целым числом.
    if type(min_length) is not int or min_length < 1:
        raise ValueError("Минимальная длина должна быть положительным целым числом.")

    # Нарушения накапливаются независимо, поэтому можно сообщить о нескольких условиях
    # одновременно.
    errors = []
    # Длина измеряется числом символов строки.
    if len(password) < min_length:
        errors.append(f"Нужно хотя бы {min_length} символов.")
    # Проверяется наличие хотя бы одной строчной латинской буквы.
    if not any(character in string.ascii_lowercase for character in password):
        errors.append("Нужна строчная латинская буква.")
    # Проверяется наличие хотя бы одной прописной латинской буквы.
    if not any(character in string.ascii_uppercase for character in password):
        errors.append("Нужна заглавная латинская буква.")
    # Проверяется наличие хотя бы одной цифры ASCII.
    if not any(character in string.digits for character in password):
        errors.append("Нужна цифра от 0 до 9.")
    # Специальный символ должен принадлежать заданному набору.
    if not any(character in SPECIAL_CHARACTERS for character in password):
        errors.append(f"Нужен символ из {SPECIAL_CHARACTERS}.")
    # Пустой список означает выполнение всех проверяемых условий.
    return errors


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for password in ("school", "SchoolProject7!"):
        errors = check_password_rules(password)
        print(f"Учебный пароль {password!r}")
        if errors:
            for error in errors:
                print("-", error)
        else:
            print("Все учебные правила выполнены.")
