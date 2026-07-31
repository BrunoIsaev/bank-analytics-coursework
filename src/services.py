"""Модуль с сервисами для анализа транзакций."""

import re
from typing import List, Dict, Any, Optional

import pandas as pd


def get_top_cashback_categories(
    data: List[Dict[str, Any]], year: int, month: int
) -> Dict[str, float]:
    """Анализирует выгодность категорий для повышенного кешбэка.

    Args:
        data: Список словарей с транзакциями.
        year: Год для анализа.
        month: Месяц для анализа.

    Returns:
        Словарь {категория: сумма_трат} за указанный месяц.
    """
    # Фильтруем по году и месяцу
    filtered = [
        t for t in data
        if t.get("Дата операции", "").year == year and
           t.get("Дата операции", "").month == month
    ]

    # Группируем траты по категориям
    category_spending = {}
    for t in filtered:
        cat = t.get("Категория", "Прочее")
        amount = abs(t.get("Сумма операции", 0))
        category_spending[cat] = category_spending.get(cat, 0) + amount

    # Возвращаем топ категорий (можно ограничить top-10)
    return dict(sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:10])


def investment_bank(
    month: str, transactions: List[Dict[str, Any]], limit: int
) -> float:
    """Рассчитывает сумму для Инвесткопилки через округление трат.

    Args:
        month: Месяц в формате 'YYYY-MM'.
        transactions: Список словарей с транзакциями.
        limit: Порог округления (10, 50 или 100).

    Returns:
        Общая сумма, накопленная в копилке за месяц.
    """
    total_saved = 0.0
    year, m = map(int, month.split("-"))

    for t in transactions:
        date = t.get("Дата операции")
        if hasattr(date, 'year') and date.year == year and date.month == m:
            amount = abs(t.get("Сумма операции", 0))
            # Округляем вверх до ближайшего кратного limit
            rounded = ((int(amount) // limit) + 1) * limit
            saved = rounded - amount
            total_saved += saved

    return round(total_saved, 2)


def simple_search(transactions: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Ищет транзакции по подстроке в описании или категории (без учета регистра).

    Args:
        transactions: Список транзакций.
        query: Поисковый запрос.

    Returns:
        Список найденных транзакций.
    """
    query_lower = query.lower()
    results = []
    for t in transactions:
        desc = str(t.get("Описание", "")).lower()
        cat = str(t.get("Категория", "")).lower()
        if query_lower in desc or query_lower in cat:
            results.append(t)
    return results


def search_by_phone(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ищет транзакции с телефонными номерами в описании.

    Поддерживает форматы: +7 (900) 000-00-00, 89000000000 и др.

    Args:
        transactions: Список транзакций.

    Returns:
        Список транзакций с телефонами.
    """
    # Regex для российских номеров
    phone_pattern = re.compile(
        r'(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    )
    results = []
    for t in transactions:
        desc = str(t.get("Описание", ""))
        if phone_pattern.search(desc):
            results.append(t)
    return results


def search_transfers_to_persons(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ищет переводы физическим лицам.

    Критерии: категория "Переводы" и наличие имени с инициалом фамилии (например, "Иван И.").

    Args:
        transactions: Список транзакций.

    Returns:
        Список транзакций-переводов физлицам.
    """
    name_pattern = re.compile(r'[А-Яа-яЁё]+\s+[А-Яа-яЁё]\.')
    results = []
    for t in transactions:
        cat = str(t.get("Категория", ""))
        desc = str(t.get("Описание", ""))
        if "Перевод" in cat and name_pattern.search(desc):
            results.append(t)
    return results
