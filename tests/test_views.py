import json
from unittest.mock import MagicMock, patch

import pandas as pd

from src.views import get_currency_rates, get_main_page_data, get_stock_prices


def test_get_currency_rates():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Valute": {"USD": {"Value": 90.5}, "EUR": {"Value": 98.2}}
    }
    with patch("requests.get", return_value=mock_response):
        rates = get_currency_rates(["USD", "EUR"])
        assert len(rates) == 2
        assert rates[0]["currency"] == "USD"
        assert rates[0]["rate"] == 90.5


def test_get_stock_prices():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"price": 150.25}]
    with patch("requests.get", return_value=mock_response):
        prices = get_stock_prices(["AAPL"])
        assert len(prices) == 1
        assert prices[0]["stock"] == "AAPL"
        assert prices[0]["price"] == 150.25


def test_get_main_page_data():
    df = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                ["2023-05-01 10:00:00", "2023-05-15 12:00:00"]
            ),
            "Номер карты": ["*1234", "*1234"],
            "Сумма операции": [-1000.0, -500.0],
            "Сумма платежа": [-1000.0, -500.0],
            "Категория": ["Супермаркеты", "Фастфуд"],
            "Описание": ["Магазин", "Кафе"],
        }
    )
    result_json = get_main_page_data("2023-05-31 23:59:59", df)
    data = json.loads(result_json)
    assert "greeting" in data
    assert "cards" in data
    assert "top_transactions" in data
