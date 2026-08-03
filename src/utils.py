import json
import os
from datetime import datetime
from typing import Any, Dict

import pandas as pd


def load_transactions(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        print(f"Файл не найден: {filepath}")
        return pd.DataFrame()
    try:
        df = pd.read_excel(filepath)
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(
                df["Дата операции"], dayfirst=True, errors="coerce"
            )
        return df
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return pd.DataFrame()


def get_greeting(date_str: str | None = None) -> str:
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.now()
    else:
        dt = datetime.now()

    hour = dt.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour <= 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings(filepath: str = "user_settings.json") -> Dict[str, Any]:
    if not os.path.exists(filepath):
        return {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
        }
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
        }
