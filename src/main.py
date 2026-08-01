"""Главный модуль приложения для анализа банковских транзакций."""

import os
import sys
import json
import logging
from src.utils import load_transactions, load_user_settings, get_greeting
from src.views import get_main_page_data
from src.services import (
    get_top_cashback_categories,
    investment_bank,
    simple_search,
    search_by_phone,
    search_transfers_to_persons
)
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday

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


def main():
    """Основная функция приложения."""
    print("=" * 50)
    print("  Приложение для анализа банковских транзакций")
    print("=" * 50)
    
    # Загружаем данные
    # ИСПРАВЛЕНИЕ: Используем относительный путь ../data/, так как main.py в src/
    filepath = "../data/operations.xlsx"
    
    logger.info(f"Попытка загрузки данных из: {filepath}")
    df = load_transactions(filepath)
    
    if df.empty:
        logger.error("Не удалось загрузить данные или файл пуст.")
        print("Не удалось загрузить данные. Проверьте путь к файлу.")
        return

    print(f"Загружено {len(df)} транзакций.\n")
    
    # Меню выбора
    while True:
        print("Выберите действие:")
        print("1. Главная страница (JSON)")
        print("2. Поиск по описанию/категории")
        print("3. Поиск по телефонным номерам")
        print("4. Поиск переводов физлицам")
        print("5. Анализ кешбэка по категориям")
        print("6. Расчет Инвесткопилки")
        print("7. Отчет: траты по категории")
        print("8. Отчет: траты по дням недели")
        print("9. Отчет: рабочие vs выходные")
        print("0. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "1":
            # Используем новую функцию из views.py
            logger.info("Генерация данных для главной страницы")
            main_page_data = get_main_page_data(df)
            print(json.dumps(main_page_data, indent=2, ensure_ascii=False))
            
        elif choice == "2":
            query = input("Введите запрос для поиска: ")
            results = simple_search(df, query)
            print(f"Найдено {len(results)} совпадений.")
            
        elif choice == "3":
            phone = input("Введите номер телефона: ")
            results = search_by_phone(df, phone)
            print(f"Найдено {len(results)} переводов.")
            
        elif choice == "4":
            name = input("Введите имя получателя: ")
            results = search_transfers_to_persons(df, name)
            print(f"Найдено {len(results)} переводов.")
            
        elif choice == "5":
            report = get_top_cashback_categories(df)
            print("\nТоп категорий по кешбэку:")
            print(report)
            
        elif choice == "6":
            settings = load_user_settings()
            report = investment_bank(df, settings)
            print("\nРасчет Инвесткопилки:")
            print(report)
            
        elif choice == "7":
            report = spending_by_category(df)
            print("\nТраты по категориям:")
            print(report)
            
        elif choice == "8":
            report = spending_by_weekday(df)
            print("\nСредние траты по дням недели:")
            print(report)
            
        elif choice == "9":
            report = spending_by_workday(df)
            print("\nСредние траты по типу дня:")
            print(report)
            
        elif choice == "0":
            print("Выход из программы.")
            break
            
        else:
            print("Некорректный выбор. Попробуйте снова.")
            
        print("\n" + "-" * 50)

if __name__ == "__main__":
    main()
