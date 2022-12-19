from pprint import pprint

from src.main_page import MainPage
from src.detail_page import DetailPage


def main():
    url = f"https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D9%86%D9%82%D9%84%DB%8C%D9%87/%D8%AE%D9%88%D8%AF%D8%B1%D9%88"
    data: list = MainPage.fetch_main_page_data(url)
    output = list()
    for obj in data:
        url = obj.get('link')
        detail = DetailPage.fetch_detail_page_data(url)
        obj.update(detail)
        output.append(obj)
    return output


# pprint(main())
if __name__ == '__main__':
    main()
