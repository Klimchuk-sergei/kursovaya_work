import json
from typing import Any, Dict, List

import pandas as pd

from Src.config import logger


def get_profitable_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Функция Анализирует, в каких категориях наиболее выгодный кешбэк.

    Возвращает JSON с категориями и суммами возможного кешбэка.
    """
    try:
        df = pd.DataFrame(data)

        # Преобразовываем дату и фильтруем данные по году и месяцу
        df['Дата операции'] = pd.to_datetime(df['Дата операции'].str.split().str[0], format="%d.%m.%Y")
        df = df[df['Дата операции'].dt.year == year]
        df = df[df['Дата операции'].dt.month == month]

        # Получаем только расходы (отрицательыне суммы операций)
        df['Сумма операции'] = pd.to_numeric(df['Сумма операции'], errors='coerce')
        df = df[df['Сумма операции'] < 0]

        # Группируем по категориям и расчитыаем кешбэк (1% от расходов)
        result = (
            df.groupby("Категория")["Сумма операции"]
            .sum()
            .abs()
            .map(lambda x: round(x / 100, 2))  # 1% кешбэк
            .sort_values(ascending=False)
            .to_dict()
        )

        logger.info(f"Кешбэк по категориям за {month}/{year} рассчитан.")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка при анализе кешбэка: {e}")
        return json.dumps({"error": "Ошибка анализа данных."})
