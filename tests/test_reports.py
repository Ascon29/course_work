import pytest

from src.reports import filtering_by_category, filtering_by_date

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
            "11.12.2020 00:00:00",
            [
                {"Дата платежа": "10.10.2020", "Сумма платежа": -200, "Категория": "Аптеки"},
                {"Дата платежа": "11.11.2020", "Сумма платежа": 1200, "Категория": "Такси"},
            ],
        ),
        (test_data, "01.01.2023 00:00:00", []),
    ],
)
def test_filtering_by_date(dat, date, expected):
    assert filtering_by_date(dat, date) == expected
