import pandas as pd

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


def get_sample_df():
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                ["2023-05-01 10:00:00", "2023-05-15 12:00:00"]
            ),
            "Категория": ["Супермаркеты", "Фастфуд"],
            "Сумма операции": [-1000.0, -500.0],
            "Описание": ["Покупка 1", "Покупка 2"],
        }
    )


def test_spending_by_category():
    df = get_sample_df()
    res = spending_by_category(df, "Супермаркеты", "2023-05-31 23:59:59")
    assert isinstance(res, pd.DataFrame)
    assert len(res) == 1


def test_spending_by_category_no_results():
    df = get_sample_df()
    res = spending_by_category(df, "Такси", "2023-05-31 23:59:59")
    assert len(res) == 0


def test_spending_by_weekday():
    df = get_sample_df()
    res = spending_by_weekday(df, "2023-05-31 23:59:59")
    assert isinstance(res, pd.DataFrame)
    assert "Средняя сумма" in res.columns


def test_spending_by_workday():
    df = get_sample_df()
    res = spending_by_workday(df, "2023-05-31 23:59:59")
    assert isinstance(res, pd.DataFrame)
    assert "Средняя сумма" in res.columns
