# Приложение для анализа банковских транзакций

Курсовая работа по анализу данных банковских операций на Python.

## Структура проекта

bank-analytics-coursework/
├── src/
│   ├── init.py
│   ├── main.py           # Главный модуль приложения
│   ├── utils.py          # Загрузка данных, приветствие
│   ├── views.py          # Главная страница (JSON)
│   ├── services.py       # Поиск и анализ транзакций
│   └── reports.py        # Отчёты по категориям и дням
├── tests/
│   ├── init.py
│   ├── test_utils.py
│   ├── test_views.py
│   ├── test_services.py
│   └── test_reports.py
├── data/
│   └── operations.xlsx   # Excel файл с транзакциями
├── logs/
│   └── coursework.log    # Логи приложения
├── user_settings.json    # Настройки пользователя (валюты, акции)
├── .env_template         # Шаблон переменных окружения
├── .gitignore            # Файлы для игнорирования Git
└── README.md             # Этот файл

## Установка

1. Клонируй репозиторий:
```bash
git clone <твой_репозиторий>
cd bank-analytics-coursework
cat > tests/test_utils.py << 'EOF'
"""Тесты для модуля utils."""
import os
import json
import pytest
import pandas as pd
from datetime import datetime
from src.utils import load_transactions, load_user_settings, get_greeting


def test_load_user_settings_default(tmp_path):
    """Тест загрузки настроек по умолчанию, если файл не найден."""
    settings = load_user_settings(str(tmp_path / "nonexistent.json"))
    assert settings["user_currencies"] == ["USD", "EUR"]
    assert settings["user_stocks"] == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_load_user_settings_from_file(tmp_path):
    """Тест загрузки настроек из существующего файла."""
    settings_file = tmp_path / "settings.json"
    test_settings = {"user_currencies": ["GBP"], "user_stocks": ["AAPL"]}
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(test_settings, f)

    loaded = load_user_settings(str(settings_file))
    assert loaded == test_settings


def test_get_greeting_morning():
    """Тест приветствия в утреннее время (06:00–11:59)."""
    dt = datetime(2021, 12, 20, 9, 0, 0)
    assert get_greeting(dt) == "Доброе утро"


def test_get_greeting_afternoon():
    """Тест приветствия в дневное время (12:00–17:59)."""
    dt = datetime(2021, 12, 20, 14, 0, 0)
    assert get_greeting(dt) == "Добрый день"


def test_get_greeting_evening():
    """Тест приветствия в вечернее время (18:00–22:59)."""
    dt = datetime(2021, 12, 20, 19, 0, 0)
    assert get_greeting(dt) == "Добрый вечер"


def test_get_greeting_night():
    """Тест приветствия в ночное время (23:00–05:59)."""
    dt = datetime(2021, 12, 20, 23, 30, 0)
    assert get_greeting(dt) == "Доброй ночи"
    
    dt = datetime(2021, 12, 20, 3, 0, 0)
    assert get_greeting(dt) == "Доброй ночи"
