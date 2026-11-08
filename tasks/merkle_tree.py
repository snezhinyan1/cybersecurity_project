# Проверка включения элемента в учебном дереве Меркла по пути от листа до доверенного корня.

import hashlib
import sys


def hash_node(left, right):
    # Хэш родителя вычисляется от конкатенации шестнадцатеричных хэшей левого и правого потомков.
    return hashlib.sha256((left + right).encode()).hexdigest()


def verify_merkle_proof(target_tx_hash, proof_path, merkle_root):
    # Вычисление начинается с хэша проверяемого листа.
    current_hash = target_tx_hash

    # Каждый элемент доказательства содержит соседний хэш и признак его расположения слева.
    for sibling_hash, is_left in proof_path:
        if is_left:
            # Левый хэш передаётся первым, поскольку порядок потомков влияет на результат.
            current_hash = hash_node(sibling_hash, current_hash)
        else:
            # Если сосед расположен справа, текущий хэш передаётся первым.
            current_hash = hash_node(current_hash, sibling_hash)

    # Доказательство принимается при совпадении вычисленного корня с доверенным значением.
    return current_hash == merkle_root


# Демонстрационный блок выполняется только при запуске модуля как программы.
if __name__ == "__main__":
    # Если поток поддерживает настройку, для вывода кириллицы используется UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Хэши четырёх демонстрационных транзакций образуют листья дерева.
    h1 = hashlib.sha256(b"TX1").hexdigest()
    h2 = hashlib.sha256(b"TX2").hexdigest()
    h3 = hashlib.sha256(b"TX3").hexdigest()
    h4 = hashlib.sha256(b"TX4").hexdigest()

    # Попарное объединение листьев образует промежуточный уровень и затем корень.
    h12 = hash_node(h1, h2)
    h34 = hash_node(h3, h4)
    real_root = hash_node(h12, h34)

    # Для третьего листа указываются четвёртый лист справа и левая ветвь уровнем выше.
    proof_for_tx3 = [
        (h4, False),
        (h12, True),
    ]

    # Проверка восстанавливает корневой хэш по указанному пути.
    is_valid = verify_merkle_proof(h3, proof_for_tx3, real_root)
    print(f"Статус верификации узла TX3: {is_valid}")
