import pandas as pd

from src.utils import get_greeting, load_transactions, load_user_settings


def test_load_transactions_not_found():
    df = load_transactions("non_existent_file.xlsx")
    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_get_greeting_time_slots():
    assert get_greeting("2023-01-01 08:00:00") == "Доброе утро"
    assert get_greeting("2023-01-01 14:00:00") == "Добрый день"
    assert get_greeting("2023-01-01 20:00:00") == "Добрый вечер"
    assert get_greeting("2023-01-01 02:00:00") == "Доброй ночи"
    valid_greetings = ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]
    assert get_greeting("invalid_date_format") in valid_greetings


def test_load_user_settings_not_found():
    settings = load_user_settings("missing_config.json")
    assert "user_currencies" in settings
    assert "user_stocks" in settings
