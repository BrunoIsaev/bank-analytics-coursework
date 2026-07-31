"""Главный модуль приложения для анализа транзакций."""

import json
from typing import Dict, Any

import pandas as pd

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


def main():
    """Основная функция приложения."""
    print("=" * 50)
    print("  Приложение для анализа банковских транзакций")
    print("=" * 50)

    # Загружаем данные
    filepath = "data/operations.xlsx"
    df = load_transactions(filepath)

    if df.empty:
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
            date_str = input("Введите дату (YYYY-MM-DD HH:MM:SS) или Enter для текущей: ").strip()
            if not date_str:
                from datetime import datetime
                date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = get_main_page_data(date_str, df)
            print("\nJSON-ответ для главной страницы:")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif choice == "2":
            query = input("Введите поисковый запрос: ").strip()
            results = simple_search(df.to_dict("records"), query)
            print(f"\nНайдено {len(results)} транзакций:")
            for r in results[:5]:
                print(f"  - {r.get('Описание', '')} ({r.get('Категория', '')})")

        elif choice == "3":
            results = search_by_phone(df.to_dict("records"))
            print(f"\nНайдено {len(results)} транзакций с телефонами:")
            for r in results[:5]:
                print(f"  - {r.get('Описание', '')}")

        elif choice == "4":
            results = search_transfers_to_persons(df.to_dict("records"))
            print(f"\nНайдено {len(results)} переводов физлицам:")
            for r in results[:5]:
                print(f"  - {r.get('Описание', '')}")

        elif choice == "5":
            year = int(input("Год: "))
            month = int(input("Месяц (1-12): "))
            results = get_top_cashback_categories(df.to_dict("records"), year, month)
            print("\nТоп категорий по тратам:")
            for cat, amount in list(results.items())[:5]:
                print(f"  {cat}: {amount:.2f} руб.")

        elif choice == "6":
            month_str = input("Месяц (YYYY-MM): ").strip()
            limit = int(input("Порог округления (10/50/100): "))
            saved = investment_bank(month_str, df.to_dict("records"), limit)
            print(f"\nСумма в Инвесткопилке: {saved:.2f} руб.")

        elif choice == "7":
            category = input("Название категории: ").strip()
            report = spending_by_category(df, category)
            print(f"\nТраты по категории '{category}': {len(report)} операций")
            print(report[["Дата операции", "Сумма операции", "Описание"]].head())

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
