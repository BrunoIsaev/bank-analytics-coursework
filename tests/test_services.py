"""Тесты для модуля services."""

import json

import pytest

from src.services import (
    investment_bank,
    search_by_phone,
    search_transfers_to_persons,
    simple_search,
)


@pytest.fixture
def sample_transactions():
    """Фиксчур: примерные транзакции."""
    from datetime import datetime

    return [
        {
            "Дата операции": datetime(2021, 5, 10, 10, 0, 0),
            "Сумма операции": -100.0,
            "Описание": "Оплата в Яндекс.Такси",
            "Категория": "Транспорт",
        },
        {
            "Дата операции": datetime(2021, 5, 15, 14, 30, 0),
            "Сумма операции": -50.0,
            "Описание": "Перевод И.В. И. +79999999999",
            "Категория": "Переводы",
        },
        {
            "Дата операции": datetime(2021, 5, 20, 16, 45, 0),
            "Сумма операции": -200.0,
            "Описание": "Ресторан Сушия",
            "Категория": "Еда",
        },
    ]


def test_simple_search(sample_transactions):
    """Тест простого поиска по описанию."""
    result = simple_search(sample_transactions, "Такси")
    data = json.loads(result)

    assert len(data) == 1
    assert "Такси" in data[0]["Описание"]


def test_simple_search_case_insensitive(sample_transactions):
    """Тест поиска без учёта регистра."""
    result = simple_search(sample_transactions, "такси")
    data = json.loads(result)

    assert len(data) == 1


def test_simple_search_empty(sample_transactions):
    """Тест поиска без результатов."""
    result = simple_search(sample_transactions, "Несуществующее")
    data = json.loads(result)

    assert len(data) == 0


def test_search_by_phone(sample_transactions):
    """Тест поиска по телефонному номеру."""
    result = search_by_phone(sample_transactions)
    data = json.loads(result)

    assert len(data) == 1
    assert "+79999999999" in data[0]["Описание"]


def test_search_transfers_to_persons(sample_transactions):
    """Тест поиска переводов физлицам."""
    result = search_transfers_to_persons(sample_transactions)
    data = json.loads(result)

    assert len(data) == 1
    assert data[0]["Категория"] == "Переводы"


def test_investment_bank(sample_transactions):
    """Тест расчёта Инвесткопилки."""
    total = investment_bank("2021-05", sample_transactions, limit=100)

    # Проверяем, что расчёт работает (результат — число >= 0)
    assert isinstance(total, float)
    assert total >= 0
