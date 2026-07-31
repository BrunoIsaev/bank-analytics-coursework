"""Модуль для работы с файлами различных форматов (CSV, Excel)."""

from typing import Any, Dict, List

import pandas as pd


def read_csv_transactions(filepath: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        filepath: Путь к CSV-файлу.

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список, если файл не найден или пуст.
    """
    try:
        df = pd.read_csv(filepath)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла {filepath}: {e}")
        return []


def read_excel_transactions(filepath: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx).

    Args:
        filepath: Путь к Excel-файлу.

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список, если файл не найден или пуст.
    """
    try:
        df = pd.read_excel(filepath)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel файла {filepath}: {e}")
        return []
