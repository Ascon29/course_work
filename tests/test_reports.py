import pandas as pd
import pytest

from src.reports import filtering_by_category, filtering_by_date, log

test_data = [
    {"Дата платежа": "08.08.2020", "Сумма платежа": -1000, "Категория": "Супермаркеты"},
    {"Дата платежа": "09.09.2020", "Сумма платежа": -1900, "Категория": "Дом и ремонт"},
    {"Дата платежа": "10.10.2020", "Сумма платежа": -200, "Категория": "Аптеки"},
    {"Дата платежа": "11.11.2020", "Сумма платежа": 1200, "Категория": "Такси"},
    {"Дата платежа": "01.01.2024", "Сумма платежа": -150, "Категория": "Фастфуд"},
]


@pytest.mark.parametrize(
    "dat, cat, expected",
    [
        (
            test_data,
            "Супермаркеты",
            [{"Дата платежа": "08.08.2020", "Сумма платежа": -1000, "Категория": "Супермаркеты"}],
        ),
        (test_data, "skypro", []),
    ],
)
def test_filtering_by_category(dat, cat, expected):
    assert filtering_by_category(dat, cat) == expected


@pytest.mark.parametrize(
    "dat, date, expected",
    [
        (
            test_data,
            "2020-11-12 00:00:00",
            [
                {"Дата платежа": "09.09.2020", "Сумма платежа": -1900, "Категория": "Дом и ремонт"},
                {"Дата платежа": "10.10.2020", "Сумма платежа": -200, "Категория": "Аптеки"},
                {"Дата платежа": "11.11.2020", "Сумма платежа": 1200, "Категория": "Такси"},
            ],
        ),
        (test_data, "2023-01-01 00:00:00", []),
    ],
)
def test_filtering_by_date(dat, date, expected):
    assert filtering_by_date(dat, date) == expected


test_data_for_log = [
    {"Дата платежа": "08.10.2020", "Сумма платежа": -1000, "Категория": "Супермаркеты"},
    {"Дата платежа": "09.09.2020", "Сумма платежа": -1900, "Категория": "Супермаркеты"},
]


def test_spending_by_category():
    @log()
    def spending_by_category(dat, cat, date):
        return pd.DataFrame(test_data_for_log)

    result = spending_by_category(test_data, "Супермаркеты", "2020-10-10 00:00:00")
    assert result == test_data_for_log
