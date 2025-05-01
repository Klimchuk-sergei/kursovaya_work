import json
from unittest.mock import MagicMock, patch

from Src.views import generate_main_page_response


@patch("Src.views.filter_transactions_by_date")
@patch("Src.views.get_currency_rates")
@patch("Src.views.get_sp500_stock_prices")
def test_generate_main_page_response_success(mock_stocks, mock_rates, mock_filter_transactions):
    mock_filter_transactions.return_value = MagicMock()
    mock_filter_transactions.return_value.columns = ["Дата операции", "Сумма платежа", "Категория", "Описание",
                                                     "Номер карты", "Сумма операции"]
    mock_filter_transactions.return_value.__getitem__.side_effect = lambda x: MagicMock()

    mock_rates.return_value = [
        {"currency": "USD", "rate": 75.0},
        {"currency": "EUR", "rate": 90.0}
    ]

    mock_stocks.return_value = [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3300.0}
    ]

    response = generate_main_page_response("2021-12-31 12:00:00")
    data = json.loads(response)

    assert isinstance(data, dict)
    assert "greeting" in data
    assert "cards" in data
    assert "top_transactions" in data
    assert "currency_rates" in data
    assert "stock_prices" in data
