import json
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from Src.config import logger


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> str:
    """
    Функция подсчитввает средние траты за каждый день недели за последние 3 месяца.

    Возвращает JSON ответ с днями недели и средними тратами.
    """
    try:
        if date:
            end_date = datetime.strptime(date, "%Y-%m-%d")
        else:
            end_date = datetime.today()

        start_date = end_date - timedelta(days=90)

        df = transactions.copy()
        df["Дата операции"] = pd.to_datetime(df["Дата операции"].str.split().str[0], format="%d.%m.%Y")
        df["Сумма операции"] = pd.to_numeric(df["Сумма операции"], errors="coerce")

        # Фильтрация: только последние 3 месяца и только траты
        df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
        df = df[df["Сумма операции"] < 0]

        day_map = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье"
        }

        df["День недели"] = df["Дата операции"].dt.weekday.map(day_map)
        avg_spending = df.groupby("День недели")["Сумма операции"].mean().abs().round(2)

        ordered_days = list(day_map.values())
        result = {}
        for day in ordered_days:
            if day in avg_spending:
                result[day] = avg_spending[day]

        logger.info("Отчёт по тратам по дням недели сформирован.")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в spending_by_weekday: {e}")
        return json.dumps({"error": "Не удалось сформировать отчёт"})

        # # Добавляем колонку: день недели
        # df["День недели"] = df["Дата операции"].dt.day_name(locale="ru_RU")
        #
        # # Считаем средние траты по дню недели
        # weekday_stats = df.groupby("День недели")["Сумма операции"].mean().abs().round(2)
        #
        # # Преобразуем в словарь и JSON
        # result = weekday_stats.to_dict()
        # logger.info("Отчёт по тратам по дням недели сформирован.")
        # return json.dumps(result, ensure_ascii=False, indent=2)

    # except Exception as e:
    #     import traceback
    #     logger.error("Ошибка в spending_by_weekday:\n" + traceback.format_exc())
    #     return json.dumps({"error": "Не удалось сформировать отчёт"})

    # except Exception as e:
    #     logger.error(f"Ошибка в отчёте по дням недели: {e}")
    #     return json.dumps({"error": "Не удалось сформировать отчёт"})
