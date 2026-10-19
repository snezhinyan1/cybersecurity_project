#  Структура данных "Дерево Меркла".
#  Реализация древовидной структуры хэширования. Метод применяется в распределенных
#  системах для эффективной верификации целостности отдельного элемента данных без необходимости
#  вычисления контрольных сумм всего массива.

import hashlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def hash_node(left, right):
    # Конкатенация данных двух дочерних узлов и вычисление криптографического хэша родительского узла.
    return hashlib.sha256((left + right).encode()).hexdigest()


def verify_merkle_proof(target_tx_hash, proof_path, merkle_root):
    current_hash = target_tx_hash

    # Итеративный подъем по ветви дерева от целевого узла к корневому.
    for sibling_hash, is_left in proof_path:
        if is_left:
            # Вычисление хэша в случае левостороннего расположения соседнего узла.
            current_hash = hash_node(sibling_hash, current_hash)
        else:
            # Вычисление хэша в случае правостороннего расположения соседнего узла.
            current_hash = hash_node(current_hash, sibling_hash)

    # Сопоставление вычисленного корневого хэша с эталонным значением структуры.
    return current_hash == merkle_root


# Моделирование генерации транзакций и вычисления их первичных хэшей.
h1 = hashlib.sha256(b"TX1").hexdigest()
h2 = hashlib.sha256(b"TX2").hexdigest()
h3 = hashlib.sha256(b"TX3").hexdigest()
h4 = hashlib.sha256(b"TX4").hexdigest()

# Построение промежуточных узлов и вычисление эталонного корня дерева Меркла.
h12 = hash_node(h1, h2)
h34 = hash_node(h3, h4)
real_root = hash_node(h12, h34)

# Формирование маршрута доказательства для верификации конкретной транзакции.
proof_for_tx3 = [
    (h4, False),
    (h12, True),
]

# Вызов функции верификации.
is_valid = verify_merkle_proof(h3, proof_for_tx3, real_root)
print(f"Статус верификации узла TX3: {is_valid}")
