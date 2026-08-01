"""Модуль с утилитами для курсовой работы."""

import os
import json
import logging
import pandas as pd
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/coursework.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_transactions(filepath: str = None) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла.
    
    Args:
        filepath: Путь к файлу operations.xlsx. 
                  По умолчанию: ../data/operations.xlsx
        
    Returns:
        DataFrame с транзакциями.
    """
    if filepath is None:
        # Используем относительный путь от src/ к data/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        filepath = os.path.join(project_root, "data", "operations.xlsx")
    
    logger.info(f"Загрузка транзакций из файла: {filepath}")
    
    try:
        df = pd.read_excel(filepath)
        logger.info(f"Успешно загружено {len(df)} транзакций")
        
        # Исправляем парсинг дат: убираем жесткий формат, используем dayfirst
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
            logger.info("Даты успешно распарсены")
            
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке транзакций: {e}")
        raise


def load_user_settings(filepath: str = None) -> dict:
    """Загружает настройки пользователя из JSON-файла.
    
    Args:
        filepath: Путь к файлу user_settings.json.
                  По умолчанию: ../user_settings.json
        
    Returns:
        Словарь с настройками.
    """
    if filepath is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        filepath = os.path.join(project_root, "user_settings.json")
    
    logger.info(f"Загрузка настроек пользователя из: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        logger.info("Настройки пользователя успешно загружены")
        return settings
    except Exception as e:
        logger.error(f"Ошибка при загрузке настроек: {e}")
        # Возвращаем дефолтные настройки, чтобы программа не падала
        return {"currency": "RUB", "language": "ru"}


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"
