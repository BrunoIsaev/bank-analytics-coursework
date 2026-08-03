import json
import os
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import get_greeting, load_user_settings

load_dotenv()


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    rates = []
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=5)
        if response.status_code == 200:
            data = response.json()
            for curr in currencies:
                if curr in data.get("Valute", {}):
                    rates.append(
                        {
                            "currency": curr,
                            "rate": round(float(data["Valute"][curr]["Value"]), 2),
                        }
                    )
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    prices = []
    api_key = os.getenv("API_KEY", "demo")
    for stock in stocks:
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote-short/{stock}?apikey={api_key}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and response.json():
                price = float(response.json()[0]["price"])
                prices.append({"stock": stock, "price": round(price, 2)})
            else:
                prices.append({"stock": stock, "price": 100.0})
        except Exception:
            prices.append({"stock": stock, "price": 100.0})
    return prices


def get_main_page_data(date_str: str, transactions_df: pd.DataFrame) -> str:
    greeting = get_greeting(date_str)

    dt_end = pd.to_datetime(date_str)
    dt_start = dt_end.replace(day=1, hour=0, minute=0, second=0)

    df_filtered = transactions_df[
        (transactions_df["Дата операции"] >= dt_start)
        & (transactions_df["Дата операции"] <= dt_end)
    ].copy()

    cards_data = []
    if "Номер карты" in df_filtered.columns and not df_filtered.empty:
        df_expenses = df_filtered[df_filtered["Сумма операции"] < 0]
        for card_num, group in df_expenses.groupby("Номер карты"):
            card_str = str(card_num).replace(".0", "").strip()
            if card_str and card_str != "nan":
                total_spent = abs(group["Сумма операции"].sum())
                cards_data.append(
                    {
                        "last_digits": card_str[-4:],
                        "total_spent": round(float(total_spent), 2),
                        "cashback": round(float(total_spent * 0.01), 2),
                    }
                )

    top_transactions = []
    if "Сумма платежа" in df_filtered.columns and not df_filtered.empty:
        sorted_df = df_filtered.sort_values(
            by="Сумма платежа", key=abs, ascending=False
        ).head(5)
        for _, row in sorted_df.iterrows():
            top_transactions.append(
                {
                    "date": row["Дата операции"].strftime("%d.%m.%Y"),
                    "amount": round(float(row["Сумма платежа"]), 2),
                    "category": str(row.get("Категория", "")),
                    "description": str(row.get("Описание", "")),
                }
            )

    settings = load_user_settings()

    result = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)
