import json
from unittest.mock import patch

import pytest

from Src.services import get_profitable_cashback_categories


@pytest.fixture
def sample_data():
    return [
        {
            "Дата операции": "15.12.2021 12:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": "-100.00"
        },
        {
            "Дата операции": "20.12.2021 15:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": "-200.00"
        },
        {
            "Дата операции": "25.12.2021 18:00:00",
            "Категория": "Фастфуд",
            "Сумма операции": "-50.00"
        },
        {
            "Дата операции": "30.11.2021 10:00:00",
            "Категория": "Фастфуд",
            "Сумма операции": "-500.00"
        }
    ]


@patch("Src.services.logger")
def test_cashback_calculation(mock_logger, sample_data):
    result_json = get_profitable_cashback_categories(sample_data, 2021, 12)
    result = json.loads(result_json)

    # Проверяем структуру и значеия
    assert isinstance(result, dict)
    assert result["Супермаркеты"] == 3.0
    assert result["Фастфуд"] == 0.5
    assert len(result) == 2

    # Проверяем логирование
    mock_logger.info.assert_called_once_with("Кешбэк по категориям за 12/2021 рассчитан.")


@patch("Src.services.logger")
def test_cashback_invalid_data_returns_error(mock_logger):
    # Передаём невалидные данные — не хватит нужных столбцов
    broken_data = [{"непонятное поле": "что-то не то"}]

    result_json = get_profitable_cashback_categories(broken_data, 2021, 12)
    result = json.loads(result_json)

    # Проверка: должен вернуться словарь с ключом "error"
    assert isinstance(result, dict)
    assert "error" in result
    assert "ошибка" in result["error"].lower()

    # Проверка вызова логирования ошибки
    mock_logger.error.assert_called_once()
