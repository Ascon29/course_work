import json
from unittest.mock import patch

import pytest

from src.views import main_page_function

operations = [
    {
        "Дата операции": "18.11.2021 21:15:27",
        "Дата платежа": "19.11.2021",
        "Номер карты": "*7951",
        "Статус": "OK",
        "Сумма операции": -200.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -200.0,
        "Валюта платежа": "RUB",
        "Категория": "Мобильная связь",
        "Описание": "Тинькофф Мобайл +7 995 555-55-55",
        "Бонусы (включая кэшбэк)": 2,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 200.0,
    }
]

expect = [
    {
        "greeting": "Доброе утро",
        "cards": [{"last_digits": "7951", "total_spent": -200, "cashback": 2.0}],
        "top_transactions": [
            {
                "date": "19.11.2021",
                "amount": -200.0,
                "category": "Мобильная связь",
                "description": "Тинькофф Мобайл +7 995 555-55-55",
            }
        ],
        "currency_rates": [{"currency": "USD", "rate": 85.5}, {"currency": "EUR", "rate": 95.5}],
        "stock_prices": [{"stock": "AAPL", "price": 150.12}, {"stock": "AMZN", "price": 3173.18}],
    }
]
expected_json = json.dumps(expect, ensure_ascii=False, indent=4)


@patch("src.views.get_stocks")
@patch("src.views.get_currencies")
@patch("src.views.get_user_settings")
@patch("src.views.top_five_operations")
@patch("src.views.get_operations")
@patch("src.views.greetings")
def test_main_page_function(
    mock_greetings,
    mock_get_operations,
    mock_top_five_operations,
    mock_get_user_settings,
    mock_get_currencies,
    mock_get_stocks,
):

    mock_greetings.return_value = {"greeting": "Доброе утро"}
    mock_get_operations.return_value = [{"last_digits": "7951", "total_spent": -200, "cashback": 2.0}]
    mock_top_five_operations.return_value = [
        {
            "date": "19.11.2021",
            "amount": -200.0,
            "category": "Мобильная связь",
            "description": "Тинькофф Мобайл +7 995 555-55-55",
        }
    ]
    mock_get_user_settings.return_value = (["USD", "EUR"], ["AAPL", "AMZN"])
    mock_get_currencies.return_value = [{"currency": "USD", "rate": 85.5}, {"currency": "EUR", "rate": 95.5}]
    mock_get_stocks.return_value = [{"stock": "AAPL", "price": 150.12}, {"stock": "AMZN", "price": 3173.18}]

    assert main_page_function("2021-11-17 11:15:27") == expected_json


def test_main_page_function_exception():
    with pytest.raises(Exception) as exception:
        main_page_function("SKYPRO")
        assert exception.value == f"Произошла ошибка {exception}"
