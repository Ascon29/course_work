import json
import os
import datetime
from collections import defaultdict

from src.excel_reader import read_excel_to_dataframe
from config import ROOT_DIR, DATA_DIR
import requests
from dotenv import load_dotenv


def get_time_now():
    '''
    функция для определения текущего времени
    :return: время в формате %Y-%m-%d %H:%M:%S
    '''
    time_now = datetime.datetime.now()
    current_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


def greetings(time=get_time_now()):
    '''
    функция приветствует пользователя в зависимости от текущего времени
    :param time: текущее время от get_time_now()
    :return: словарь
    '''
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    hours = time.hour
    if 6 <= hours < 12:
        greeting = "Доброе утро"
    elif 12 <= hours < 18:
        greeting = "Добрый день"
    elif 18 <= hours < 24:
        greeting = "Добрый вечер"
    else:
        greeting = "Добрая ночь"
    greeting_time = {"greeting": greeting}
    return greeting_time


def filtering_operations_by_date(operations=read_excel_to_dataframe(DATA_DIR + "/operations.xls"), date_now='2021-11-12 12:36:09'):
    '''
    функция фильтрует операции по текущей дате, так же отсеивает операции без даты платежа и если операция не прошла
    :param date_now: текущая дата и время
    :param operations: DataFrame
    :return: отфильтрованный список словарей
    '''
    date_now = datetime.datetime.strptime(date_now, "%Y-%m-%d %H:%M:%S")
    operations_data = operations.to_json(orient="records")
    data_py = json.loads(operations_data)
    filter_by_date = []
    for data in data_py:
        if data['Дата платежа'] and data['Статус'] == 'OK':
            date_payment = datetime.datetime.strptime(data['Дата платежа'], '%d.%m.%Y')
            if date_now.year == date_payment.year and date_now.month == date_payment.month and date_now.day >= date_payment.day:
                filter_by_date.append(data)
    return filter_by_date


def get_operations():
    '''
    функция использует отфильтрованный список по дате filtering_operations_by_date() и возвращает По каждой карте:
            - последние 4 цифры карты;
            - общая сумма расходов;
            - кешбэк (1 рубль на каждые 100 рублей)
    :return: список словарей
    '''
    operations = filtering_operations_by_date()
    card_numbers = list(set(i['Номер карты'] for i in operations if i['Номер карты'] is not None))
    payments = defaultdict(int)
    for card_number in card_numbers:
        for operation in operations:
            if operation['Номер карты'] == card_number and operation['Сумма платежа'] < 0:
                payments[card_number] += round(operation['Сумма платежа'])

    result = []
    for payment in payments:
        result.append({"last_digits": payment[1:],
                       "total_spent": payments[payment],
                       "cashback": abs(payments[payment]) / 100})
    return result


def top_five_operations():
    '''
    функция использует отфильтрованный список по дате filtering_operations_by_date()
    возвращает топ-5 транзакций по сумме платежа
    :return: список словарей
    '''
    operations = filtering_operations_by_date()
    sorted_operations = sorted(operations, key=lambda x: x["Сумма операции"], reverse=True)[0:5]
    result = []
    for operation in sorted_operations:
        result.append({"date": operation["Дата платежа"],
                       "amount": operation["Сумма платежа"],
                       "category": operation["Категория"],
                       "description": operation["Описание"]})
    return result


def get_user_settings(settings=ROOT_DIR + '/user_settings.json'):
    '''
    конвертирует json-объект в python
    :param settings: путь до файла валютой и акциями
    :return: словарь
    '''
    with open(settings, "r", encoding="utf-8") as file:
        user_settings = json.load(file)
        return user_settings


def get_currencies(user_currencies=get_user_settings()):
    '''
    принимает настройки пользователя в виде python-объекта
    возвращает курсы валют
    :param user_currencies: словарь с курсами валют
    :return: список курса валют полученный через API
    '''
    load_dotenv()
    url = "https://api.apilayer.com/exchangerates_data/latest"
    API_KEY = os.getenv("API_KEY_CURS")
    headers = {"apikey": API_KEY}
    result = []

    for i in user_currencies['user_currencies']:
        params = {"base": i, "sumbols": "RUB"}
        response = requests.get(url, headers=headers, params=params)
        response_result = response.json()
        result.append({"currency": i, "rate": response_result["rates"]["RUB"]})

    return result


def get_stocks(user_stocks=get_user_settings()):
    '''
    принимает настройки пользователя в виде python-объекта
    :param user_stocks: словарь с акции
    :return: список цен на акции полученные через API
    '''
    load_dotenv()
    API_KEY = os.getenv("API_KEY_STOCKS")
    result = []

    for i in user_stocks['user_stocks']:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={i}&apikey={API_KEY}'
        response = requests.get(url)
        response_result = response.json()
        result.append({'stock': i, 'price': response_result['Global Quote']['05. price']})

    return result


# if __name__ == '__main__':


    # print(get_stocks(get_user_settings()))
    # print(get_currencies(get_user_settings()))
    # print(get_user_settings())
    # print(top_five_operations())
    # print(greetings(get_time_now()))
    # print(get_operations())
    # print(get_user_settings(ROOT_DIR + '/user_settings.json'))
    # print(get_currencies(get_user_settings))
