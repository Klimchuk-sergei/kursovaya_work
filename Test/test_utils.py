import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from Src.utils import (
    load_transactions,
    filter_transactions_by_date,
    get_currency_rates,
    get_sp500_stock_prices,
    get_greeting
)


@pytest.fixture
def mock_transactions():
    data = {
        "Дата операции": ["01.12.2021 12:00:00", "15.12.2021 12:00:00", "31.12.2021 12:00:00"],
        "Номер карты": ["*5814", "*5824", "*7512"],
        "Сумма операции": [-100.0, -200.0, 300.0],
        "Сумма платежа": [100.0, 200.0, 300.0],
        "Категория": ["Супермаркеты", "Фастфуд", "Переводы"],
        "Описание": ["Пятерочка", "Бургер Кинг", "Перевод другу"]
    }
    return pd.DataFrame(data)


@patch("pandas.read_excel")
def test_load_transactions_success(mock_read_excel, mock_transactions):
    mock_read_excel.return_value = mock_transactions
    result = load_transactions()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


@patch("Src.utils.load_transactions")
def test_filter_transactions_by_date(mock_load_transactions, mock_transactions):
    mock_load_transactions.return_value = mock_transactions
    filtered = filter_transactions_by_date("2021-12-31")
    assert isinstance(filtered, pd.DataFrame)
    assert not filtered.empty
    assert filtered.shape[0] == 3


@patch("Src.utils.yf.Ticker")
def test_get_currency_rates(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame({"Close": [75.0]})
    mock_ticker.return_value = mock_instance

    rates = get_currency_rates()
    assert isinstance(rates, list)
    assert rates[0]["currency"] == "USD"
    assert isinstance(rates[0]["rate"], float)


@patch("Src.utils.yf.Ticker")
def test_get_sp500_stock_prices(mock_ticker):
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame({"Close": [100.0]})
    mock_ticker.return_value = mock_instance

    prices = get_sp500_stock_prices()
    assert isinstance(prices, list)
    assert prices[0]["stock"] == "AAPL"
    assert isinstance(prices[0]["price"], float)


@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (8, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (2, "Доброй ночи"),
    ]
)
def test_get_greeting(hour, expected_greeting):
    test_time = pd.Timestamp(year=2021, month=12, day=1, hour=hour)
    greeting = get_greeting(test_time)
    assert greeting == expected_greeting
