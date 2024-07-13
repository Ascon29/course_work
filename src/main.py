from excel_reader import read_excel_to_dataframe, read_excel_to_list
from reports import spending_by_category
from services import searching_by_phone_numbers
from utils import get_time_now
from views import main_page_function


def main():
    print(main_page_function())
    time_now = get_time_now()
    print(time_now)
    operations_list = read_excel_to_list()
    print("-----------------------------------")
    print(searching_by_phone_numbers(operations_list))
    print("-----------------------------------")
    operations_dataframe = read_excel_to_dataframe()
    category = "супермаркет"
    date_filter = "2021-07-13 04:20:34"
    print(spending_by_category(operations_dataframe, category, date=date_filter))
    print("-----------------------------------")


main()
