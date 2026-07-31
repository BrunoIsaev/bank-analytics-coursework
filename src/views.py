"""Модуль для генерации JSON-ответов веб-страниц."""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

import pandas as pd
import requests

from src.utils import load_user_settings, get_greeting


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получает курсы валют через API ЦБ РФ.

    Args:
        currencies: Список кодов валют (например, ["USD", "EUR"]).

    Returns:
        Список словарей с ключами 'currency' и 'rate'.
    """
    rates = []
    try:
        # Используем открытый API ЦБ РФ
        response = requests.get(
            "https://www.cbr-xml-daily.ru/daily_json.js", timeout=10
        )
        data = response.json()
        for curr in currencies:
            if curr in data["Valute"]:
                rates.append({
                    "currency": curr,
                    "rate": data["Valute"][curr]["Value"]
                })
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Получает цены акций через API Yahoo Finance (альтернатива).

    Args:
        stocks: Список тикеров акций (например, ["AAPL", "TSLA"]).

    Returns:
        Список словарей с ключами 'stock' и 'price'.
    """
    prices = []
    # Для простоты используем mock-данные, так как бесплатные API акций часто требуют ключей
    # В реальном проекте здесь был бы запрос к Alpha Vantage или Yahoo Finance
    mock_prices = {
        "AAPL": 150.12, "AMZN": 3173.18, "GOOGL": 2742.39,
        "MSFT": 296.71, "TSLA": 1007.08
    }
    for stock in stocks:
        price = mock_prices.get(stock, 0.0)
        if price > 0:
            prices.append({"stock": stock, "price": price})
    return prices


def get_main_page_data(
    date_str: str, transactions_df: pd.DataFrame
) -> Dict[str, Any]:
    """Генерирует JSON-ответ для главной страницы.

    Args:
        date_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'.
        transactions_df: DataFrame с транзакциями.

    Returns:
        Словарь с данными для главной страницы.
    """
    # 1. Приветствие
    greeting = get_greeting(date_str)

    # 2. Данные по картам (группируем по номеру карты)
    cards_data = []
    if "Номер карты" in transactions_df.columns and "Сумма операции" in transactions_df.columns:
        grouped = transactions_df.groupby("Номер карты")
        for card_num, group in grouped:
            total_spent = abs(group["Сумма операции"].sum())
            cashback = round(total_spent * 0.01, 2)  # 1% кешбэк
            last_digits = str(card_num)[-4:] if len(str(card_num)) >= 4 else str(card_num)
            cards_data.append({
                "last_digits": last_digits,
                "total_spent": round(total_spent, 2),
                "cashback": cashback
            })

    # 3. Топ-5 транзакций по сумме платежа
    top_transactions = []
    if "Сумма платежа" in transactions_df.columns:
        sorted_df = transactions_df.sort_values(
            by="Сумма платежа", ascending=False
        ).head(5)
        for _, row in sorted_df.iterrows():
            date_fmt = row["Дата операции"].strftime("%d.%m.%Y") if pd.notna(row["Дата операции"]) else ""
            top_transactions.append({
                "date": date_fmt,
                "amount": round(float(row["Сумма платежа"]), 2),
                "category": row.get("Категория", ""),
                "description": row.get("Описание", "")
            })

    # 4. Курсы валют и акции из настроек
    settings = load_user_settings()
    currency_rates = get_currency_rates(settings.get("user_currencies", []))
    stock_prices = get_stock_prices(settings.get("user_stocks", []))

    return {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
