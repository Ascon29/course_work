import json

from src.utils import greetings, get_operations, top_five_operations, get_currencies, get_stocks


def main_page_function():
    '''
    функция для запуска главной страницы
    :return: json-ответ
    '''
    result = []
    result_dict = {}
    result_dict.update(greetings())
    result_dict.update({"cards": get_operations()})
    result_dict.update({"top_transactions": top_five_operations()})
    # result.update({"currency_rates": get_currencies()})
    # result.update({"stock_prices": get_stocks()})
    result.append(result_dict)
    result_json = json.dumps(result, ensure_ascii=False, indent=4)

    return result_json


if __name__ == '__main__':
    print(main_page_function())
