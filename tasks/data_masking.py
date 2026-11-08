# Маскирование адреса электронной почты перед журналированием. Сохранённые признаки адреса могут
# позволить идентифицировать владельца.

import string
import sys


def mask_email(email):
    """Принимает простой ASCII-адрес local@domain с точкой в домене."""
    # Предварительная проверка обеспечивает однозначное разделение адреса на две части.
    if not isinstance(email, str) or email.count("@") != 1:
        raise ValueError("Ожидается адрес вида local@domain.")
    local, domain = email.split("@")
    # Набор допустимых символов локальной части ограничен учебным ASCII-форматом.
    allowed_local = string.ascii_letters + string.digits + "._+-"
    if not local or any(character not in allowed_local for character in local):
        raise ValueError("Недопустимая личная часть адреса.")
    # Начальная, конечная или повторная точка образует пустой сегмент локальной части.
    if local.startswith(".") or local.endswith(".") or ".." in local:
        raise ValueError("Точки должны разделять непустые части имени.")

    # Домен разбивается на метки для независимой проверки каждой части.
    labels = domain.split(".")
    if len(labels) < 2:
        raise ValueError("Домен должен содержать точку.")
    for label in labels:
        # Пустые метки и дефисы на границах меток отклоняются.
        if not label or label.startswith("-") or label.endswith("-"):
            raise ValueError("Недопустимая часть домена.")
        # Для каждой метки проверяется допустимый алфавит.
        if any(character not in string.ascii_letters + string.digits + "-" for character in label):
            raise ValueError("Домен должен состоять из ASCII-букв, цифр и дефисов.")

    # Единственный символ скрывается полностью, чтобы локальная часть не раскрывалась целиком.
    if len(local) == 1:
        return "***@" + domain
    # Фиксированное число звёздочек не раскрывает длину скрытой части имени.
    return local[0] + "***@" + domain


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for address in ("student@example.org", "a@example.org"):
        print("Адрес для журнала:", mask_email(address))
