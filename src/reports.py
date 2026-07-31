"""Модуль с отчетами по транзакциям."""

import functools
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

import pandas as pd


def save_report(filename: Optional[str] = None):
    """Декоратор для сохранения результата функции-отчета в Excel-файл.

    Args:
        filename: Имя файла для сохранения. Если None, используется имя функции + дата.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Генерируем имя файла, если не передано
            if filename is None:
                date_str = datetime.now().strftime("%Y%m%d")
                file_name = f"{func.__name__}_{date_str}.xlsx"
            else:
                file_name = filename
            
            # Сохраняем DataFrame в Excel
            if isinstance(result, pd.DataFrame):
                result.to_excel(file_name, index=False)
                print(f"Отчет сохранен в файл: {file_name}")
            else:
                print("Результат функции не является DataFrame, сохранение пропущено.")
            
            return result
        return wrapper
    return decorator


@save_report()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями.
        category: Название категории.
        date: Дата отсчета (YYYY-MM-DD). Если None, берется текущая дата.

    Returns:
        DataFrame с транзакциями указанной категории.
    """
    if date:
        end_date = pd.to_datetime(date)
    else:
        end_date = pd.datetime.now()
    
    start_date = end_date - pd.DateOffset(months=3)
    
    # Фильтруем по дате и категории
    mask = (
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= end_date) &
        (transactions["Категория"] == category)
    )
    
    return transactions[mask].copy()


@save_report()
def spending_by_weekday(
    transactions: pd.DataFrame,
    date: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает средние траты по дням недели за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями.
        date: Дата отсчета (YYYY-MM-DD). Если None, берется текущая дата.

    Returns:
        DataFrame со средними тратами по дням недели.
    """
    if date:
        end_date = pd.to_datetime(date)
    else:
        end_date = pd.datetime.now()
    
    start_date = end_date - pd.DateOffset(months=3)
    
    # Фильтруем по дате
    filtered = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= end_date)
    ].copy()
    
    # Добавляем день недели
    filtered["День недели"] = filtered["Дата операции"].dt.day_name()
    
    # Группируем и считаем среднее
    result = filtered.groupby("День недели")["Сумма операции"].mean().reset_index()
    result.columns = ["День недели", "Средняя сумма"]
    
    return result


@save_report()
def spending_by_workday(
    transactions: pd.DataFrame,
    date: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает средние траты в рабочие и выходные дни за последние 3 месяца.

    Args:
        transactions: DataFrame с транзакциями.
        date: Дата отсчета (YYYY-MM-DD). Если None, берется текущая дата.

    Returns:
        DataFrame со средними тратами по типу дня.
    """
    if date:
        end_date = pd.to_datetime(date)
    else:
        end_date = pd.datetime.now()
    
    start_date = end_date - pd.DateOffset(months=3)
    
    # Фильтруем по дате
    filtered = transactions[
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= end_date)
    ].copy()
    
    # Определяем тип дня (0-4: будни, 5-6: выходные)
    filtered["Тип дня"] = filtered["Дата операции"].dt.dayofweek.apply(
        lambda x: "Рабочий день" if x < 5 else "Выходной"
    )
    
    # Группируем и считаем среднее
    result = filtered.groupby("Тип дня")["Сумма операции"].mean().reset_index()
    result.columns = ["Тип дня", "Средняя сумма"]
    
    return result
