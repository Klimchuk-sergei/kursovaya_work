from Src.reports import spending_by_weekday
from Src.services import get_profitable_cashback_categories
from Src.utils import get_stock_prices, load_transactions
from Src.views import generate_main_page_response

if __name__ == "__main__":
    # Загружаем транзакции
    transactions = load_transactions()

    print("Проверка yfinance")
    print(get_stock_prices())

    # Страница "Главная"
    print("▷ Главная страница:")
    print(generate_main_page_response("2021-12-31 12:00:00"))

    # Отчёт по дням недели
    print("\n▷▷ Траты по дням недели:")
    print(spending_by_weekday(transactions, "2021-12-11"))

    # Выгодные категории кешбэка
    print("\n▷▷▷ Выгодные категории кешбэка:")
    print(get_profitable_cashback_categories(transactions.to_dict(orient="records"), 2021, 12))
