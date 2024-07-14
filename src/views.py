import json
import logging

from config import LOGS_VIEWS_DIR
from excel_reader import read_excel_to_list
from src.utils import (filtering_operations_by_date, get_currencies, get_operations, get_stocks, get_user_settings,
                       greetings, top_five_operations)

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOGS_VIEWS_DIR, "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s -%(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_page_function(date):
    """
    функция для запуска главной страницы
    :return: json-ответ
    """
    try:
        logger.info("Функция начала раюоту. Запускает набор функций, необходимых для работы")
        greeting = greetings(date)
        data_from_json = read_excel_to_list()
        filtered_data = filtering_operations_by_date(data_from_json, date)
        card_operations = get_operations(filtered_data)
        top_five = top_five_operations(filtered_data)
        user_settings = get_user_settings()
        user_currencies = get_currencies(user_settings[0])
        user_stocks = get_stocks(user_settings[1])

        logger.info("Все подфункции отработали. Идет запись данных в словарь")
        result_dict = {}
        result_dict.update(greeting)
        result_dict.update({"cards": card_operations})
        result_dict.update({"top_transactions": top_five})
        result_dict.update({"currency_rates": user_currencies})
        result_dict.update({"stock_prices": user_stocks})

        logger.info("Словарь с данными создан. Функция создает список и конвертирует его в json-ответ")
        result = [result_dict]
        result_json = json.dumps(result, ensure_ascii=False, indent=4)
        logger.info("Функция успешно завершила работу")
        return result_json
    except Exception as e:
        logger.error(f"Произошла ошибка {e}")


if __name__ == "__main__":
    print(main_page_function())
