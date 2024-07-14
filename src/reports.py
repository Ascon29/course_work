import datetime
import json
import logging
import os.path
import re
from functools import wraps

import pandas as pd

from config import DATA_DIR, LOGS_REPORTS_DIR

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOGS_REPORTS_DIR, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s -%(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def log(filename="spending.json"):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs).to_dict(orient="records")
            with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            return result

        return inner

    return wrapper


def filtering_by_category(operations, category):
    """
    Функция фильтрует операции по заданной категории, так же отсеивает операции без категорий
    :param operations: DataFrame с операциями
    :param category: заданная пользователем категория
    :return: отфильтрованный список словарей
    """
    logger.info("Функция начала работу.")
    result = []
    logger.info("Функция отсеивает пустые категории и переводит результат в словарь")
    pattern = category
    logger.info("Функция записывает операции с выбранной категорией в список")
    for i in operations:
        if re.findall(pattern, i["Категория"], flags=re.IGNORECASE):
            result.append(i)
    logger.info("Функция успешно завершила работу")
    return result


def filtering_by_date(operations, date):
    """
    Функция фильтрует операции по дате. возвращает операции за последние 3 месяца от указанной даты
    :param operations: список операций (отфильтрованный по категории)
    :param date: optional. Если дата не указана, применяется функция получения текущей даты
    :return: отфильтрованный список словарей
    """
    logger.info("Функция начала работу")
    result = []
    date_get = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    deadline = date_get - datetime.timedelta(days=90)
    logger.info("Функция фильтрует операции за последние 3 месяца")
    for operation in operations:
        payment_date = datetime.datetime.strptime(operation["Дата платежа"], "%d.%m.%Y")
        if deadline <= payment_date <= date_get:
            result.append(operation)
    logger.info("Функция успешно завершила работу")
    return result


@log()
def spending_by_category(operations_df, category, date):
    """
    Функция для подсчета трат по заданной категории в течении 3-х месяцев от заданной даты.
    если дата не указана, использует текущую
    :param operations_df: DataFrame с операциями
    :param category: выбранная пользователем категория
    :param date: введенная дата (опционально)
    :return: DataFrame
    """
    operations_with_category = operations_df.loc[operations_df["Категория"].notnull()].to_dict(orient="records")
    filter_by_cat = filtering_by_category(operations_with_category, category)
    filter_by_dat = filtering_by_date(filter_by_cat, date)
    return pd.DataFrame(filter_by_dat)
