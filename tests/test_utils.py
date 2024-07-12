import os
from unittest.mock import patch

import pytest

from src.utils import (filtering_operations_by_date, get_currencies, get_operations, get_stocks, get_user_settings,
                       greetings, top_five_operations)


def test_greeting_with_conftest(test_greeteng):
    assert greetings("2021-11-12 06:00:00") == test_greeteng


@pytest.mark.parametrize(
    "time, expected",
    [
        ("2021-11-12 06:00:00", {"greeting": "Доброе утро"}),
        ("2021-11-12 13:00:00", {"greeting": "Добрый день"}),
        ("2021-11-12 20:00:00", {"greeting": "Добрый вечер"}),
        ("2021-11-12 02:00:00", {"greeting": "Добрая ночь"}),
    ],
)
def test_greeting(time, expected):
    assert greetings(time) == expected


@pytest.mark.parametrize(
    "data, time, expected",
    [
        (
            [
                {
                    "Дата операции": "12.11.2021 19:29:24",  # ожидаемый результат
                    "Дата платежа": "12.11.2021",
                    "Номер карты": "*4556",
                    "Статус": "OK",
                    "Сумма операции": -250.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -250.0,
                    "Валюта платежа": "RUB",
                },
                {
                    "Дата операции": "12.11.2021 19:29:24",
                    "Дата платежа": "12.11.2021",
                    "Номер карты": "*4556",
                    "Статус": "FAILED",  # проверка на отсеивание статуса FAILED
                    "Сумма операции": -250.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -250.0,
                    "Валюта платежа": "RUB",
                },
                {
                    "Дата операции": "12.11.2021 19:29:24",
                    "Дата платежа": "",  # проверка на отсеивание даты платежа без значения
                    "Номер карты": "*4556",
                    "Статус": "OK",
                    "Сумма операции": -250.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -250.0,
                    "Валюта платежа": "RUB",
                },
            ],
            "2021-11-13 12:36:09",
            [
                {
                    "Дата операции": "12.11.2021 19:29:24",
                    "Дата платежа": "12.11.2021",
                    "Номер карты": "*4556",
                    "Статус": "OK",
                    "Сумма операции": -250.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -250.0,
                    "Валюта платежа": "RUB",
                }
            ],
        ),
        (
            [
                {
                    "Дата операции": "12.11.2021 19:29:24",  # проверка на отсеивание по дате
                    "Дата платежа": "12.11.2021",
                    "Номер карты": "*4556",
                    "Статус": "OK",
                    "Сумма операции": -250.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -250.0,
                    "Валюта платежа": "RUB",
                }
            ],
            "2021-11-11 12:36:09",
            [],
        ),
    ],
)
def test_filtering_operations_by_date(data, time, expected):
    assert filtering_operations_by_date(data, time) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [
                {"Номер карты": "*7197", "Сумма платежа": -250.0},
                {
                    "Номер карты": "*4556",
                    "Сумма платежа": -83.0,
                },
            ],
            [  # КОНКРЕТНО ЭТА ЧАСТЬ ТЕСТА ПРОХОДИТ ЧЕРЕЗ РАЗ, ПОТОМУ ЧТО ФУНКЦИЯ ИСПОЛЬЗУЕТ МНОЖЕСТВО
                {"last_digits": "4556", "total_spent": -83, "cashback": 0.83},
                {"last_digits": "7197", "total_spent": -250, "cashback": 2.5},
            ],
        ),
        (
            [
                {"Номер карты": "*7197", "Сумма платежа": 100.0},
                {"Номер карты": "*4556", "Сумма платежа": -83.0},
            ],
            [{"last_digits": "4556", "total_spent": -83, "cashback": 0.83}],
        ),
    ],
)
def test_get_operations(data, expected):
    assert get_operations(data) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [
                {"Дата платежа": "12.11.2021", "Сумма платежа": -250.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": -1000.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": 27.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": -350.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": 500.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": -150.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": -1.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": 1.0, "Категория": "Др", "Описание": "Сити"},
                {"Дата платежа": "12.11.2021", "Сумма платежа": 125.0, "Категория": "Др", "Описание": "Сити"},
            ],
            [
                {"date": "12.11.2021", "amount": -1000.0, "category": "Др", "description": "Сити"},
                {"date": "12.11.2021", "amount": 500.0, "category": "Др", "description": "Сити"},
                {"date": "12.11.2021", "amount": -350.0, "category": "Др", "description": "Сити"},
                {"date": "12.11.2021", "amount": -250.0, "category": "Др", "description": "Сити"},
                {"date": "12.11.2021", "amount": -150.0, "category": "Др", "description": "Сити"},
            ],
        )
    ],
)
def test_top_five_operations(data, expected):
    assert top_five_operations(data) == expected


@patch("json.load")
def test_get_user_settings(mock_json):
    mock_json.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }
    assert get_user_settings() == (["USD", "EUR"], ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])


@patch("requests.get")
@patch.dict(os.environ, {"API_KEY_CURS": "api_key"})
def test_get_currencies(mock_get):
    mock_get.return_value.json.return_value = {
        "base": "USD",
        "date": "2024-07-11",
        "rates": {
            "RUB": 85.5,
        },
    }
    assert get_currencies(["USD"]) == [{"currency": "USD", "rate": 85.5}]
    mock_get.assert_called_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": "api_key"},
        params={"base": "USD", "sumbols": "RUB"},
    )


@patch("requests.get")
def test_get_currencies_with_ex(mock_request):
    mock_request.return_value.status_code = 400
    mock_request.return_value.json.return_value = {
        "base": "USD",
        "date": "2024-07-11",
        "rates": {
            "RUB": 85.5,
        },
    }
    with pytest.raises(Exception) as exception:
        get_stocks("JPY")
        assert exception.value == f"Произошла ошибка {exception}"


@patch("requests.get")
@patch.dict(os.environ, {"API_KEY_STOCKS": "api_key"})
def test_get_stocks(mock_get):
    mock_get.return_value.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "176.6000",
            "03. high": "178.2200",
            "04. low": "174.4500",
            "05. price": "177.8400",
        }
    }
    assert get_stocks(["AAPL"]) == [{"stock": "AAPL", "price": 177.84}]
    mock_get.assert_called_with("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=api_key")


@patch("requests.get")
def test_get_stocks_with_ex(mock_request):
    mock_request.return_value.status_code = 400
    mock_request.return_value.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "176.6000",
            "03. high": "178.2200",
            "04. low": "174.4500",
            "05. price": "177.8400",
        }
    }
    with pytest.raises(Exception) as exception:
        get_stocks("SKYPRO")
        assert exception.value == f"Произошла ошибка {exception}"
