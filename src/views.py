"""Модуль представлений для генерации данных главной страницы."""

import logging
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def filter_current_month(df: pd.DataFrame) -> pd.DataFrame:
    """Фильтрует транзакции за текущий месяц (с 1-го числа по сегодня).
    
    Args:
        df: DataFrame со всеми транзакциями.
        
    Returns:
        Отфильтрованный DataFrame.
    """
    if df.empty or "Дата операции" not in df.columns:
        logger.warning("DataFrame пуст или отсутствует колонка дат")
        return df
        
    today = pd.Timestamp.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Фильтруем: дата >= начала месяца И дата <= сегодня
    mask = (df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= today)
    filtered_df = df[mask].copy()
    
    logger.info(f"Отфильтровано {len(filtered_df)} транзакций за текущий месяц")
    return filtered_df


def process_cards(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Группирует транзакции по картам и считает суммы/количество.
    
    Args:
        df: DataFrame с транзакциями за текущий месяц.
        
    Returns:
        Список словарей с информацией по каждой карте.
    """
    if df.empty or "Карта" not in df.columns:
        return []
        
    cards_data = []
    grouped = df.groupby("Карта")
    
    for card_name, group in grouped:
        total_spent = group["Сумма"].sum()
        count = len(group)
        cards_data.append({
            "card": str(card_name),
            "total_spent": round(total_spent, 2),
            "transactions_count": count
        })
        
    logger.info(f"Обработано {len(cards_data)} карт")
    return sorted(cards_data, key=lambda x: x["total_spent"], reverse=True)


def process_top_transactions(df: pd.DataFrame, top_n: int = 5) -> List[Dict[str, Any]]:
    """Формирует топ-N самых дорогих транзакций.
    
    Args:
        df: DataFrame с транзакциями за текущий месяц.
        top_n: Количество транзакций в топе.
        
    Returns:
        Список словарей с топ-транзакциями.
    """
    if df.empty:
        return []
        
    # Сортируем по сумме убыванию и берем первые N
    top_df = df.nlargest(top_n, "Сумма")
    
    result = []
    for _, row in top_df.iterrows():
        result.append({
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "description": row.get("Описание", "Без описания"),
            "amount": round(row["Сумма"], 2),
            "category": row.get("Категория", "Прочее")
        })
        
    logger.info(f"Сформирован топ-{top_n} транзакций")
    return result


def get_stock_prices() -> List[Dict[str, Any]]:
    """Возвращает котировки акций (заглушка/Mock).
    
    Поскольку реальное API может быть недоступно или требовать ключ,
    используем статические данные для демонстрации функционала.
    
    Returns:
        Список словарей с котировками.
    """
    logger.info("Получение котировок акций (используется заглушка)")
    
    # Статические данные вместо реального API запроса
    mock_stocks = [
        {"ticker": "SBER", "price": 285.40, "change": 1.2},
        {"ticker": "GAZP", "price": 168.90, "change": -0.5},
        {"ticker": "LKOH", "price": 7250.00, "change": 0.8},
        {"ticker": "YNDX", "price": 3450.50, "change": 2.1}
    ]
    
    return mock_stocks


def get_main_page_data(transactions_df: pd.DataFrame) -> Dict[str, Any]:
    """Собирает все данные для отображения на главной странице.
    
    Args:
        transactions_df: DataFrame со ВСЕМИ транзакциями (неотфильтрованными).
        
    Returns:
        Словарь с данными для фронтенда/вывода.
    """
    logger.info("Начало сборки данных для главной страницы")
    
    # 1. Сначала фильтруем по текущему месяцу
    current_month_df = filter_current_month(transactions_df)
    
    # 2. Обрабатываем карты
    cards = process_cards(current_month_df)
    
    # 3. Формируем топ трат
    top_transactions = process_top_transactions(current_month_df)
    
    # 4. Получаем котировки (заглушка)
    stocks = get_stock_prices()
    
    # 5. Считаем общую статистику за месяц
    total_spent = current_month_df["Сумма"].sum() if not current_month_df.empty else 0
    
    data = {
        "greeting": "Добро пожаловать в аналитику!",
        "period": "Текущий месяц",
        "total_spent": round(total_spent, 2),
        "cards": cards,
        "top_transactions": top_transactions,
        "stocks": stocks
    }
    
    logger.info("Данные для главной страницы успешно собраны")
    return data
