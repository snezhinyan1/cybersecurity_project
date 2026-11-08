# Проверка границ файлового пути после нормализации и разрешения символических ссылок.

import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def resolve_safe_path(base_directory, user_path):
    """Проверяет относительный путь, разрешая существующие символические ссылки.

    Папка должна существовать. Сам целевой файл может ещё отсутствовать.
    Проверка предполагает, что папки и ссылки не меняются между проверкой и открытием.
    """
    # Разрешённая папка должна существовать. Сравнение выполняется по её каноническому пути.
    base = Path(base_directory).resolve(strict=True)
    # Существующий файл не может служить базовым каталогом.
    if not base.is_dir():
        raise NotADirectoryError("Разрешённый путь должен указывать на папку.")

    relative_path = Path(user_path)
    # Запрещаются пути с корнем или обозначением диска, чтобы обращение оставалось относительным.
    if relative_path.anchor:
        raise ValueError("Укажите путь относительно разрешённой папки.")
    # В Windows дополнительно проверяются зарезервированные имена, включая имена устройств и
    # потоков.
    if os.name == "nt" and any(os.path.isreserved(part) for part in relative_path.parts):
        raise ValueError("Путь содержит зарезервированное Windows имя.")

    # Разрешение пути учитывает переходы к родительским каталогам и существующие символические
    # ссылки.
    target = (base / relative_path).resolve()
    try:
        # Проверяется принадлежность по компонентам пути. Совпадения строкового префикса
        # недостаточно.
        target.relative_to(base)
    except ValueError:
        raise ValueError("Выход за пределы разрешённой папки запрещён.") from None
    # Возвращается абсолютный путь, находящийся в пределах разрешённой папки.
    return target


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    with TemporaryDirectory() as folder:
        allowed = resolve_safe_path(folder, "report.txt")
        print("Разрешённое имя файла:", allowed.name)
        try:
            resolve_safe_path(folder, "../private.txt")
        except ValueError as error:
            print("Запрос отклонён.", error)
