"""Модуль для обработки банковских операций (поиск и подсчет)."""

import re
from collections import Counter
from typing import List, Dict, Any


def process_bank_search(
    data: List[Dict[str, Any]], search: str
) -> List[Dict[str, Any]]:
    """Ищет операции по заданной строке в описании
    с использованием регулярных выражений.

    Args:
        data: Список словарей с данными транзакций.
        search: Строка для поиска в поле description.

    Returns:
        Список словарей, у которых в описании
        найдена строка поиска.
    """
    result = []
    for item in data:
        desc = item.get("description", "")
        if re.search(search, desc, re.IGNORECASE):
            result.append(item)
    return result


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество операций
    по заданным категориям.

    Args:
        data: Список словарей с данными транзакций.
        categories: Список названий категорий для подсчета.

    Returns:
        Словарь, где ключи — названия категорий,
        значения — количество операций.
    """
    descriptions = [
        item.get("description", "") for item in data
    ]
    counter = Counter(descriptions)
    return {cat: counter.get(cat, 0) for cat in categories}
