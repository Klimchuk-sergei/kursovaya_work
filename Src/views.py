import json
from datetime import datetime

from Src.config import logger
from Src.utils import filter_transactions_by_date, get_currency_rates, get_greeting, get_sp500_stock_prices


def generate_main_page_response(date_time_str: str) -> str:
    """
    Формирует JSON-ответ
    """
    try:
        # Преобразуем строку даты
        current_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        # Создаем приветствие
        greeting = get_greeting(current_time)

        # Фильтрация транзакций
        filtered_df = filter_transactions_by_date(current_time.strftime("%Y-%m-%d"))
        if filtered_df is None:
            return json.dumps({"error": "Не удалось загрузить транзакции."})

        # Кешбэк и раходы по картам
        cards_info = []
        if 'Номер карты' in filtered_df.columns:
            for card in filtered_df['Номер карты'].dropna().unique():
                card_df = filtered_df[filtered_df['Номер карты'] == card]
                total_spent = card_df['Сумма операции'].apply(lambda x: x if x < 0 else 0).sum()
                cashback = round(abs(total_spent) / 100, 2)
                cards_info.append({
                    "last_digits": str(card)[-4:],  # последние 4 цифры карты
                    "total_spent": round(abs(total_spent), 2),
                    "cashback": cashback
                })

        # Топ-5 транзакций по сумме
        top_transactions = (
            filtered_df[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]
            .sort_values(by='Сумма платежа', ascending=False)
            .head(5)
            .to_dict(orient="records")
        )

        # Форматируем транзакции
        top_transactions_formatted = []
        for transaction in top_transactions:
            top_transactions_formatted.append({
                "date": transaction['Дата операции'].strftime('%d.%m.%Y'),
                "amount": round(transaction['Сумма платежа'], 2),
                "category": transaction['Категория'],
                "description": transaction['Описание']
            })

        # Курсы валют
        currency_rates = get_currency_rates()

        # Стоимости акций
        stock_prices = get_sp500_stock_prices()

        # Собираем весь JSON-ответ
        response = {
            "greeting": greeting,
            "cards": cards_info,
            "top_transactions": top_transactions_formatted,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

        logger.info("Главная страница успешно сформирована.")
        return json.dumps(response, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка при формировании главной страницы: {e}")
        return json.dumps({"error": "Внутренняя ошибка сервера."})
