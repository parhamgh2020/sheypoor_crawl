import traceback

import requests
from bs4 import BeautifulSoup
from pprint import pprint

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


base_url = "https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D9%86%D9%82%D9%84%DB%8C%D9%87/%D8%AE%D9%88%D8%AF%D8%B1%D9%88"


class MainPage:

    @classmethod
    def _get_data_class_content(cls, url):
        res = requests.get(url, allow_redirects=True, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        div_content = soup.find_all("article", class_="serp-item list")
        return div_content

    @staticmethod
    def _convert_num_to_persian(data: str):
        if not data:
            return None
        src = {
            "۰": "0",
            "۱": "1",
            "۲": "2",
            "۳": "3",
            "۴": "4",
            "۵": "5",
            "۶": "6",
            "۷": "7",
            "۸": "8",
            "۹": "9",
        }
        for k, v in src.items():
            data = data.replace(k, v)
        output = data
        for el in data:
            if el not in src.values():
                output = output.replace(el, "")
        output.replace("تومان", "").strip()
        output.replace(",", "")
        if output:
            output = int(output)
        return output

    @classmethod
    def _extract_data_article(cls, article_list):
        output = list()
        for el in article_list:
            price = el.find_all("strong", class_="item-price")[0].text
            price = None if price == "قیمت توافقی" else price
            span_list = el.find_all("span")
            span_id = [span for span in span_list if span.has_attr("data-reveal-number")][0]
            _id = span_id.attrs['data-reveal-number']
            output.append(
                    {
                        "title": el.h2.text.strip(),
                        "publish_date": el.time["datetime"],
                        "location": el.find_all("p")[1].text,
                        "price": cls._convert_num_to_persian(price) if price else price,
                        "link": el.find_all("a")[0]["href"],
                        "id": _id
                    }
                )
        return output

    @classmethod
    def fetch_main_page_data(cls, url) -> list:
        article_list = cls._get_data_class_content(url)
        output: list = cls._extract_data_article(article_list)
        return output
