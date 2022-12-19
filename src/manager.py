from pprint import pprint
from time import sleep

from src.db import DB
from src.detail_page import DetailPage
from src.main_page import MainPage
from src.db import DB
from datetime import datetime

history_id = list()


def first_step(i):
    timestamp = str(datetime.now().timestamp())
    timestamp = timestamp[:-len("0.0000")] + "0.0000"
    url = f"https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D9%86%D9%82%D9%84%DB%8C%D9%87/%D8%AE%D9%88%D8%AF%D8%B1%D9%88?p={i}&f={timestamp}"
    data: list = MainPage.fetch_main_page_data(url)
    db_data = list()
    for obj in data:
        if obj.get("id") in history_id:
            continue
        elif obj.get("id"):
            db_data.append(obj)
            history_id.append(obj.get("id"))
    if db_data:
        DB.insert_many(db_data)

    # for obj in data:
    #     url = obj.get('link')
    #     detail = DetailPage.fetch_detail_page_data(url)
    #     obj.update(detail)
    #     db_data.append(obj)
    #     pprint(obj)
    # DB.insert_many(db_data)
    # pprint(db_data)


if __name__ == '__main__':
    history_id = DB.get_last_ads_id()
    for i in range(1, 1000):
        try:
            first_step(i)
            sleep(1)
        except Exception as err:
            print(err)
            sleep(10)
        print(len(history_id))
