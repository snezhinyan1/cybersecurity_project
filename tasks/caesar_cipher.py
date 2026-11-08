# Шифр Цезаря. Латинские буквы циклически сдвигаются с сохранением регистра. Возможны 26 различных
# сдвигов.

import sys


def shift_text(text, shift):
    """Сдвигает A–Z и a–z. Остальные символы сохраняются."""
    # Сдвиг должен соответствовать целому числу позиций алфавита.
    if type(shift) is not int:
        raise ValueError("Сдвиг должен быть целым числом.")

    # Символы результата накапливаются в исходном порядке.
    result = []
    for character in text:
        # Начальный код выбирается отдельно для каждого регистра.
        if "A" <= character <= "Z":
            alphabet_start = ord("A")
        elif "a" <= character <= "z":
            alphabet_start = ord("a")
        else:
            # Символы вне латинского алфавита копируются без преобразования.
            result.append(character)
            continue

        # Вычитание кода первой буквы даёт индекс в диапазоне от 0 до 25.
        position = ord(character) - alphabet_start
        # Остаток по модулю 26 реализует циклический переход через границы алфавита.
        new_position = (position + shift) % 26
        # Индекс преобразуется обратно в символ того же регистра.
        result.append(chr(alphabet_start + new_position))
    return "".join(result)


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    message = "Document Z, version 2. Привет!"
    encrypted = shift_text(message, 3)
    print("После сдвига:", encrypted)
    # Сдвиг с противоположным знаком отменяет исходное преобразование.
    print("После обратного сдвига:", shift_text(encrypted, -3))
