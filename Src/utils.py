from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv

from Src.config import PATH_FILE, logger, sp500_tickers

load_dotenv()


def get_stock_prices() -> list:
    try:
        tickers = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        result = []

        for ticker in tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            print(f"📈 {ticker} — дата: {hist.index}, данные: {hist['Close'].values}")

            if not hist.empty:
                result.append({
                    "stock": ticker,
                    "price": round(hist["Close"].iloc[0], 2)
                })

        return result
    except Exception as e:
        print("Ошибка получения данных по акциям:", e)
        return []


def load_transactions() -> Optional[pd.DataFrame]:
    """
    Загружаем данные из exel файла
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
    Получаем актуальные курсы валют USD и EUR к RUB из библиотеки yfinance

    Возвращаем список словарей с валютами и курсами.
    """
    try:
        usd_rub = yf.Ticker("USDRUB=X").history(period="1d")['Close'].iloc[0]
        eur_rub = yf.Ticker("EURRUB=X").history(period="1d")['Close'].iloc[0]
        rates = [
            {"currency": "USD", "rate": round(usd_rub, 2)},
            {"currency": "EUR", "rate": round(eur_rub, 2)},
        ]
        logger.info("Курсы валют успешно получены.")
        return rates
    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return []


def get_sp500_stock_prices() -> List[Dict[str, float]]:
    """
    Получаем стоимость акций компаний из списка S&P500. библиоткека yfinance

    Возвращаем список словарей с акциями и их ценами.
    """
    stocks = sp500_tickers
    stock_prices = []

    try:
        for ticker in stocks:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            price = round(hist['Close'].iloc[0], 2)  # оставляем 2 знака после запятой.
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
