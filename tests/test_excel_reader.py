from unittest.mock import patch

from src.excel_reader import read_excel_to_dataframe, read_excel_to_list


@patch("pandas.read_excel")
def test_read_excel_to_list(mock_read_excel):
    mock_read_excel.return_value.to_dict.return_value = [
        {
            "Дата операции": "13.07.2021 13:13:13",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -159.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -159.0,
        }
    ]
    assert read_excel_to_list() == [
        {
            "Дата операции": "13.07.2021 13:13:13",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -159.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -159.0,
        }
    ]


@patch("pandas.read_excel")
def test_read_excel_to_dataframe(mock_read_excel):
    mock_read_excel.return_value = [
        {
            "Дата операции": "13.07.2021 13:13:13",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -159.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -159.0,
        }
    ]
    assert read_excel_to_dataframe() == [
        {
            "Дата операции": "13.07.2021 13:13:13",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -159.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -159.0,
        }
    ]
