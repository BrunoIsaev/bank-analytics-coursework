"""Модуль с утилитами для работы с данными транзакций."""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional

import pandas as pd


def load_transactions(filepath: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла в DataFrame.

    Args:
        filepath: Путь к Excel-файлу с транзакциями.

    Returns:
        DataFrame с данными транзакций.
    """
    try:
        df = pd.read_excel(filepath)
        # Приводим даты к формату datetime
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y")
        return df
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return pd.DataFrame()


def get_greeting(date_str: Optional[str] = None) -> str:
    """Возвращает приветствие в зависимости от времени суток.

    Args:
        date_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'.
                  Если None, используется текущее время.

    Returns:
        Строка приветствия: 'Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи'.
    """
    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    else:
        dt = datetime.now()

    hour = dt.hour

    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings(filepath: str = "user_settings.json") -> Dict[str, Any]:
    """Загружает пользовательские настройки из JSON-файла.

    Args:
        filepath: Путь к файлу настроек.

    Returns:
        Словарь с настройками (валюты, акции).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        print(f"Файл настроек не найден: {filepath}")
        return {"user_currencies": [], "user_stocks": []}
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON в файле {filepath}")
        return {"user_currencies": [], "user_stocks": []}
