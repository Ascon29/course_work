from unittest.mock import patch

import pytest

from src.services import searching_by_phone_numbers


@patch("json.dumps")
def test_search_by_phone_numbers(mock_dumps):
    mock_dumps.return_value = [
        {"Описание": "МТС +7 911 695-42-03"},
        {"Описание": "Я МТС +7 921 11-22-33"},
        {"Описание": "Билайн +7 962 717-08-52"},
        {"Описание": "Teletie Бизнес +7 966 000-00-00"},
    ]
    assert searching_by_phone_numbers(
        [
            {"Описание": "МТС +7 911 695-42-03"},
            {"Описание": "Я МТС +7 921 11-22-33"},
            {"Описание": "Билайн +7 962 717-08-52"},
            {"Описание": "Teletie Бизнес +7 966 000-00-00"},
            {"Описание": "Бургер Кинг"},
            {"Описание": "Метро Санкт-Петербург"},
            {"Описание": "Перевод Кредитная карта. ТП 10.2 RUR"},
            {"Описание": "Fantaziya 1"},
        ]
    ) == [
        {"Описание": "МТС +7 911 695-42-03"},
        {"Описание": "Я МТС +7 921 11-22-33"},
        {"Описание": "Билайн +7 962 717-08-52"},
        {"Описание": "Teletie Бизнес +7 966 000-00-00"},
    ]


def test_search_by_phone_numbers_empty():
    assert searching_by_phone_numbers([]) == "[]"


def test_search_by_phone_numbers_ex():
    with pytest.raises(Exception) as ex:
        searching_by_phone_numbers("")
        assert ex.value == f"Произошла ошибка {ex}"
