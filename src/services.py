import json
import math
import re
from typing import Any, Dict, List


def get_top_cashback_categories(
    data: List[Dict[str, Any]], year: int, month: int
) -> str:
    category_cashback = {}
    for t in data:
        date_raw = t.get("Дата операции")
        if (
            hasattr(date_raw, "year")
            and date_raw.year == year
            and date_raw.month == month
        ):
            cat = str(t.get("Категория", "Прочее"))
            amount = abs(float(t.get("Сумма операции", 0)))
            cashback = amount * 0.01
            category_cashback[cat] = category_cashback.get(cat, 0.0) + cashback

    sorted_cats = dict(
        sorted(category_cashback.items(), key=lambda x: x[1], reverse=True)[:3]
    )
    rounded_result = {k: round(v, 2) for k, v in sorted_cats.items()}
    return json.dumps(rounded_result, ensure_ascii=False)


def investment_bank(
    month: str, transactions: List[Dict[str, Any]], limit: int
) -> float:
    total_saved = 0.0
    try:
        year, m = map(int, month.split("-"))
    except ValueError:
        return 0.0

    for t in transactions:
        date_raw = t.get("Дата операции")
        if hasattr(date_raw, "year") and date_raw.year == year and date_raw.month == m:
            amount = float(t.get("Сумма операции", 0))
            if amount < 0:
                abs_amount = abs(amount)
                target = math.ceil(abs_amount / limit) * limit
                if target == abs_amount:
                    continue
                total_saved += target - abs_amount

    return round(total_saved, 2)


def simple_search(transactions: List[Dict[str, Any]], query: str) -> str:
    q = query.lower()
    res = []
    for t in transactions:
        if (
            q in str(t.get("Описание", "")).lower()
            or q in str(t.get("Категория", "")).lower()
        ):
            t_copy = t.copy()
            if hasattr(t_copy.get("Дата операции"), "strftime"):
                t_copy["Дата операции"] = t_copy["Дата операции"].strftime("%d.%m.%Y")
            res.append(t_copy)
    return json.dumps(res, ensure_ascii=False)


def search_by_phone(transactions: List[Dict[str, Any]]) -> str:
    phone_pattern = re.compile(
        r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
    )
    res = []
    for t in transactions:
        if phone_pattern.search(str(t.get("Описание", ""))):
            t_copy = t.copy()
            if hasattr(t_copy.get("Дата операции"), "strftime"):
                t_copy["Дата операции"] = t_copy["Дата операции"].strftime("%d.%m.%Y")
            res.append(t_copy)
    return json.dumps(res, ensure_ascii=False)


def search_transfers_to_persons(transactions: List[Dict[str, Any]]) -> str:
    pattern = re.compile(r"[А-Яа-яЁё]+\s+[А-Яа-яЁё]\.")
    res = []
    for t in transactions:
        cat = str(t.get("Категория", ""))
        desc = str(t.get("Описание", ""))
        if "Перевод" in cat and pattern.search(desc):
            t_copy = t.copy()
            if hasattr(t_copy.get("Дата операции"), "strftime"):
                t_copy["Дата операции"] = t_copy["Дата операции"].strftime("%d.%m.%Y")
            res.append(t_copy)
    return json.dumps(res, ensure_ascii=False)
