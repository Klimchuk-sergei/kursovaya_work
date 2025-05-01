# tests/test_reports.py

import json
from unittest.mock import patch

import pandas as pd
import pytest

from Src.reports import spending_by_weekday


@pytest.fixture
def weekday_data():
    return pd.DataFrame({
        "Дата операции": [
            "01.02.2024 10:00:00",  # Четверг
            "05.02.2024 12:00:00",  # Понедельник
            "12.02.2024 09:00:00",  # Понедельник
            "16.02.2024 18:00:00",  # Пятница
            "18.03.2024 15:30:00",  # Понедельник
        ],
        "Сумма операции": [
            "-100.0",
            "-50.0",
            "-150.0",
            "-200.0",
            "-300.0"
        ]
    })


@patch("Src.reports.logger")
def test_spending_by_weekday_valid(mock_logger, weekday_data):
    result_json = spending_by_weekday(weekday_data, date="2024-03-20")
    result = json.loads(result_json)

    assert isinstance(result, dict)
    assert "Понедельник" in result
    assert "Пятница" in result
    assert result["Понедельник"] == 166.67  # среднее: (50+150+300)/3
    assert result["Пятница"] == 200.0
    assert mock_logger.info.called


@patch("Src.reports.logger")
def test_spending_by_weekday_empty(mock_logger):
    df = pd.DataFrame(columns=["Дата операции", "Сумма операции"])
    result_json = spending_by_weekday(df, date="2024-03-20")
    result = json.loads(result_json)

    assert result == {}
    assert mock_logger.info.called
