# Временное ограничение попыток входа. Счётчики и сроки блокировки хранятся отдельно для каждого
# пользователя.

import math
import sys


class LoginLimiter:
    def __init__(self, max_attempts=3, block_seconds=60):
        # Порог блокировки должен быть положительным целым числом попыток.
        if type(max_attempts) is not int or max_attempts < 1:
            raise ValueError("Число попыток должно быть положительным целым.")
        # Продолжительность блокировки должна быть конечной и положительной.
        if not math.isfinite(block_seconds) or block_seconds <= 0:
            raise ValueError("Длительность блокировки должна быть положительной.")
        self.max_attempts = max_attempts
        self.block_seconds = block_seconds
        # Словарь хранит число последовательных неудач по имени пользователя.
        self.failures = {}
        # Для заблокированных пользователей хранится момент окончания ограничения.
        self.blocked_until = {}
        # Начало модельной шкалы времени соответствует нулю секунд.
        self.last_time = 0

    def can_attempt(self, username, now):
        """Время всех вызовов должно быть конечным и не убывать."""
        if not isinstance(username, str) or not username:
            raise ValueError("Укажите непустое имя пользователя.")
        # Проверка исключает неконечные значения и возврат времени к более раннему моменту.
        if not math.isfinite(now) or now < self.last_time:
            raise ValueError("Время должно быть конечным и не убывать.")
        # Принятая отметка становится нижней границей времени следующего вызова.
        self.last_time = now

        # При отсутствии записи о блокировке новая попытка разрешена.
        if username not in self.blocked_until:
            return True
        # Блокировка действует строго до указанного момента.
        if now < self.blocked_until[username]:
            return False

        # Истёкшая блокировка удаляется, а счётчик ошибок сбрасывается.
        del self.blocked_until[username]
        self.failures.pop(username, None)
        return True

    def record_result(self, username, success, now):
        """Возвращает False, если попытка отклонена из-за действующей блокировки."""
        if type(success) is not bool:
            raise ValueError("Результат входа должен быть True или False.")
        # Результат попытки во время блокировки не учитывается.
        if not self.can_attempt(username, now):
            return False

        # Успешная попытка завершает последовательность неудачных входов.
        if success:
            self.failures.pop(username, None)
        else:
            # При первой ошибке отсутствующее значение счётчика принимается равным нулю.
            failures = self.failures.get(username, 0) + 1
            self.failures[username] = failures
            # При достижении порога фиксируется абсолютный момент окончания блокировки.
            if failures >= self.max_attempts:
                self.blocked_until[username] = now + self.block_seconds
        return True


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    limiter = LoginLimiter(max_attempts=3, block_seconds=60)
    for second in (0, 1, 2):
        limiter.record_result("alice", False, second)
    print("Вход на 3-й секунде разрешён:", limiter.can_attempt("alice", 3))
    print("Вход на 62-й секунде разрешён:", limiter.can_attempt("alice", 62))
