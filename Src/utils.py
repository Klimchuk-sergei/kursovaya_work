from datetime import datetime
from typing import Optional, Dict, List
import os
import json
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from Src.config import PATH_FILE, logger

load_dotenv()

# Загрузка данные для акций икурса валют user_setings.json
USER_SETTINGS_PATH = os.path.join("Data", "user_setings.json")
with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as f:
    user_settings = json.load(f)

user_currencies = user_settings.get("user_currencies", ["USD", "EUR"])
user_stocks = user_settings.get("user_stocks", [])


def load_transactions() -> Optional[pd.DataFrame]:
    """
    Загружаем данные из excel файла
    """
    try:
        transactions = pd.read_excel(PATH_FILE)
        logger.info(f"Файл {PATH_FILE} успешно загружен.")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}")
        return None


def filter_transactions_by_date(date_str: str) -> Optional[pd.DataFrame]:
    """
    Фильтрует транзакции с начала месяца по указанную дату.

    Принимаем дату в формате 'YYYY-MM-DD'.

    Возвращаем отфильтрованный датафрейм или None при ошибке.
    """
    try:
        df = load_transactions()
        if df is None:
            return None

        end_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = end_date.replace(day=1)

        df['Дата операции'] = pd.to_datetime(df['Дата операции'].str.split().str[0], format='%d.%m.%Y')

        filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
        logger.info(f"Фильтрация транзакций с {start_date} по {end_date} выполнена успешно.")
        return filtered_df
    except Exception as e:
        logger.error(f"Ошибка при фильтрации транзакций: {e}")
        return None


def get_currency_rates() -> List[Dict[str, float]]:
    """
    Получаем актуальные курсы валют из библиотеки yfinance

    Возвращаем список словарей с валютами и курсами.
    """
    rates = []
    try:
        for currency in user_currencies:
            ticker = f"{currency}RUB=X"
            data = yf.Ticker(ticker).history(period="1d")
            if not data.empty:
                rate = data['Close'].iloc[0]
                rates.append({"currency": currency, "rate": round(rate, 2)})
        logger.info("Курсы валют успешно получены.")
        return rates
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return []


def get_sp500_stock_prices() -> List[Dict[str, float]]:
    """
    Получаем стоимость акций

    Возвращаем список словарей с акциями и их ценами.
    """
    stock_prices = []
    try:
        for ticker in user_stocks:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                price = round(hist['Close'].iloc[0], 2)
                stock_prices.append({"stock": ticker, "price": price})
        logger.info("Цены акций успешно получены.")
        return stock_prices
    except Exception as e:
        logger.error(f"Ошибка при получении цен акций: {e}")
        return []


def get_greeting(current_time: datetime) -> str:
    """
    Создаем приветствие для пользователя в зависимости от времени суток пользователя

    Возвращаем соответствующее приветствие
    """
    hour = current_time.hour
    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    logger.info(f"Приветствие сгенерировано: {greeting}")
    return greeting
