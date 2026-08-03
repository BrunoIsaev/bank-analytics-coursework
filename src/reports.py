import functools
from datetime import datetime
from typing import Callable, Optional

import pandas as pd


def save_report(filename: Optional[str] = None):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            out_file = (
                filename
                if filename
                else f"{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            if isinstance(result, pd.DataFrame):
                result.to_excel(out_file, index=False)
            return result

        return wrapper

    if callable(filename):
        f = filename
        filename = None
        return decorator(f)
    return decorator


@save_report
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    end_date = pd.to_datetime(date) if date else pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(months=3)

    mask = (
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Категория"] == category)
        & (transactions["Сумма операции"] < 0)
    )
    return transactions[mask].copy()


@save_report
def spending_by_weekday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    end_date = pd.to_datetime(date) if date else pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Сумма операции"] < 0)
    ].copy()

    filtered["Сумма операции"] = filtered["Сумма операции"].abs()
    filtered["День недели"] = filtered["Дата операции"].dt.day_name()

    res = filtered.groupby("День недели")["Сумма операции"].mean().reset_index()
    res.columns = ["День недели", "Средняя сумма"]
    return res


@save_report
def spending_by_workday(
    transactions: pd.DataFrame, date: Optional[str] = None
) -> pd.DataFrame:
    end_date = pd.to_datetime(date) if date else pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Сумма операции"] < 0)
    ].copy()

    filtered["Сумма операции"] = filtered["Сумма операции"].abs()
    filtered["Тип дня"] = filtered["Дата операции"].dt.dayofweek.apply(
        lambda x: "Рабочий день" if x < 5 else "Выходной"
    )

    res = filtered.groupby("Тип дня")["Сумма операции"].mean().reset_index()
    res.columns = ["Тип дня", "Средняя сумма"]
    return res
