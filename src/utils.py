import datetime
import json
import logging
import os
from collections import defaultdict

import requests
from dotenv import load_dotenv

from config import LOGS_UTILS_DIR, ROOT_DIR

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOGS_UTILS_DIR, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s -%(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_time_now():
    """
    функция для определения текущего времени
    :return: время в формате %Y-%m-%d %H:%M:%S
    """
    time_now = datetime.datetime.now()
    current_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def greetings(time):
    """
    функция приветствует пользователя в зависимости от текущего времени
    :param time: строка с текущим временем
    :return: словарь
    """
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    hours = time.hour
    logger.info("Функция начала обработку времени")
    if 6 <= hours < 12:
        greeting = "Доброе утро"
    elif 12 <= hours < 18:
        greeting = "Добрый день"
    elif 18 <= hours < 24:
        greeting = "Добрый вечер"
    else:
        greeting = "Добрая ночь"
    logger.info("Функция завершила работу и записала приветствие в словарь")
    greeting_time = {"greeting": greeting}
    return greeting_time


def filtering_operations_by_date(operations_data, date_now):
    """
    функция фильтрует операции по текущей дате,
    так же отсеивает операции без даты платежа и если операция не прошла (FAILED)
    :param operations_data: список операций
    :param date_now: строка с датой
    :return: отфильтрованный список операций
    """
    logger.info("Функция начала работу")
    date_now = datetime.datetime.strptime(date_now, "%Y-%m-%d %H:%M:%S")
    filter_by_date = []
    try:
        for data in operations_data:
            if data["Дата платежа"] and data["Статус"] == "OK":
                date_payment = datetime.datetime.strptime(data["Дата платежа"], "%d.%m.%Y")
                if (
                    date_now.year == date_payment.year
                    and date_now.month == date_payment.month
                    and date_now.day >= date_payment.day
                ):
                    filter_by_date.append(data)
        logger.info("Функция успешно завершила работу")
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")

    return filter_by_date


def get_operations(operations):
    """
    функция использует отфильтрованный список по дате и возвращает По каждой карте:
            - последние 4 цифры карты;
            - общая сумма расходов;
            - кешбэк (1 рубль на каждые 100 рублей)
    :param operations: отфильтрованный список словарей
    :return: список словарей
    """
    logger.info("Функция начала работу")
    card_numbers = list(set(i["Номер карты"] for i in operations if i["Номер карты"] is not None))
    payments = defaultdict(int)
    logger.info("Функция обрабатывает данные")
    for card_number in card_numbers:
        for operation in operations:
            if operation["Номер карты"] == card_number and operation["Сумма платежа"] < 0:
                payments[card_number] += round(operation["Сумма платежа"])

    result = []
    logger.info("Функция начинает формировать результат в список")
    for payment in payments:
        result.append(
            {"last_digits": payment[1:], "total_spent": payments[payment], "cashback": abs(payments[payment]) / 100}
        )
    logger.info("Функция успешно завершила работу")
    return result


def top_five_operations(operations):
    """
    функция использует отфильтрованный список по дате
    возвращает топ-5 транзакций по сумме платежа
    :param operations: отфильтрованный список словарей
    :return: список словарей
    """
    logger.info("Функция начала работу. Идет сортировка")
    sorted_operations = sorted(operations, key=lambda x: abs(x["Сумма платежа"]), reverse=True)[0:5]
    result = []
    logger.info("Функция начинает формировать результат в список")
    for operation in sorted_operations:
        result.append(
            {
                "date": operation["Дата платежа"],
                "amount": operation["Сумма платежа"],
                "category": operation["Категория"],
                "description": operation["Описание"],
            }
        )
    logger.info("Функция успешно завершила работу")
    return result


def get_user_settings():
    """
    конвертирует json-объект в python
    :return: словарь
    """
    settings = ROOT_DIR + "/user_settings.json"
    logger.info("Функция начала работу. Идет открытие json-файла")
    try:
        with open(settings, "r", encoding="utf-8") as file:
            user_settings = json.load(file)
        logger.info("Функция успешно завершила работу")
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
    return user_settings["user_currencies"], user_settings["user_stocks"]


def get_currencies(user_currencies):
    """
    использует настройки пользователя
    возвращает курсы валют
    :param: список интересующих валют
    :return: список курса валют полученный через API
    """
    logger.info("Функция начала работу")
    try:
        load_dotenv()
        url = "https://api.apilayer.com/exchangerates_data/latest"
        API_KEY = os.getenv("API_KEY_CURS")
        headers = {"apikey": API_KEY}
        result = []
        logger.info("Функция обращается к стороннему сервису для получения курса валют")
        for i in user_currencies:
            params = {"base": i, "sumbols": "RUB"}
            response = requests.get(url, headers=headers, params=params)
            response_result = response.json()
            result.append({"currency": i, "rate": round(response_result["rates"]["RUB"], 2)})
        logger.info("Функция успешно завершила работу")
        return result
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")


def get_stocks(user_stocks):
    """
    использует настройки пользователя
    :param: список интересующих акций
    :return: список цен на акции полученные через API
    """
    logger.info("Функция начала работу")
    try:
        load_dotenv()
        API_KEY = os.getenv("API_KEY_STOCKS")
        result = []
        logger.info("Функция обращается к стороннему сервису для получения цен на акции")
        for i in user_stocks:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={i}&apikey={API_KEY}"
            response = requests.get(url)
            response_result = response.json()
            result.append({"stock": i, "price": round(float(response_result["Global Quote"]["05. price"]), 2)})
        logger.info("Функция успешно завершила работу")
        return result
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")
