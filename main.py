from pprint import pprint
from time import sleep

from src.db import DB
from src.detail_page import DetailPage
from src.main_page import MainPage

lst = list()


def main(i):
    url = f"https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D9%86%D9%82%D9%84%DB%8C%D9%87/%D8%AE%D9%88%D8%AF%D8%B1%D9%88?p={i}&f=1671457430.0000"
    data: list = MainPage.fetch_main_page_data(url)
    db_data = list()
    for obj in data:
        if obj.get("id") in lst:
            continue
        else:
            lst.append(obj.get("id"))

    # for obj in data:
    #     url = obj.get('link')
    #     detail = DetailPage.fetch_detail_page_data(url)
    #     obj.update(detail)
    #     db_data.append(obj)
    #     pprint(obj)
    # DB.insert_many(db_data)
    # pprint(db_data)


if __name__ == '__main__':
    for i in range(1, 1000):
        try:
            main(i)
        except Exception as err:
            print(err)
        print(len(lst))
        sleep(10)
