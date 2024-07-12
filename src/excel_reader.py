import json

import pandas as pd

from config import DATA_DIR


def read_excel_to_dataframe(excel_file=DATA_DIR + "/operations.xls"):
    """
    конвертирует excel файл в DataFrame
    :param excel_file: путь до excel файла
    :return: DataFrame
    """
    data_frame = pd.read_excel(excel_file)
    return data_frame


def read_excel_to_list(excel_file=DATA_DIR + "/operations.xls"):
    """
    конвертирует excel файл в список
    :return: List
    """
    read = pd.read_excel(excel_file).to_json(orient="records")
    result = json.loads(read)
    return result
