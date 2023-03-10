import asyncio
import traceback
from typing import List

import requests
from bs4 import BeautifulSoup
from pprint import pprint
from bs4.element import Tag
import re
import numpy as np
from PIL import Image
import base64 as b64
import io
from src.async_requests import run_fetch


class DetailPage:

    @staticmethod
    def _get_data_page(urls) -> List[BeautifulSoup]:
        results = asyncio.run(run_fetch(urls))
        output = list()
        for http in results:
            soup = BeautifulSoup(http, 'html.parser')
            output.append(soup)
        return output

    @staticmethod
    def _tag_data(data: str):
        src = {
            "نوع شاسی": "body_type",
            "سال تولید": "production_year",
            "کیلومتر": "kilometers",
            "مدل خودرو": "sub_model",
            "رنگ": "color",
            "گیربکس": "gearbox_type",
            "نقدی/اقساطی": "payment_info",
            "نقدی": "cash",
            "اقساطی": "installments",
            "وضعیت بدنه": "body_condition",
            "نوع سوخت": "fuel_type",
        }
        return src.get(data.strip())

    @classmethod
    def _get_table_data(cls, soup: BeautifulSoup) -> dict:
        table = soup.find_all("table")
        output = dict()
        try:
            for tr in table[0]:
                if isinstance(tr, Tag):
                    output.update(
                        {cls._tag_data(tr.th.text): tr.td.text}
                    )
            for tr in table[1]:
                if isinstance(tr, Tag):
                    output.update(
                        {cls._tag_data(tr.th.text): tr.td.text}
                    )
            output = {k: v for k, v in output.items() if k}
        except:
            print(traceback.format_exc())
        return output

    @staticmethod
    def _convert_num_to_english(data: str):
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
        return data

    @classmethod
    def _get_car_brand(cls, soup: BeautifulSoup) -> str:
        nav = soup.find_all("nav", id="breadcrumbs")[0]
        li_list = nav.find_all("li")
        brand = li_list[-2].text
        return brand

    @classmethod
    def _get_description(cls, soup: BeautifulSoup) -> str:
        description_p: Tag = soup.find_all("p", id="description")[0]
        for el in description_p.find_all("span"):
            el.string = ""
        description_p_text = description_p.text.replace(
            "شماره تماس:", "").strip()
        return description_p_text

    @classmethod
    def _get_phone_by_description_url(cls, _id):
        url_description = f"https://www.sheypoor.com/api/web/listings/{_id}/description"
        res = requests.get(url_description)
        if not res.json().get("success"):
            image = res.json().get("data", dict()).get("image")
            token = res.json().get("data", dict()).get("token")
            code = CaptchaSolver.solve_captcha(image)
            headers = {"x-captcha-code": code, "x-captcha-token": token}
            res = requests.get(url_description, headers=headers)
            if res.json().get('success'):
                numbers = cls._get_phones(res.json().get('data', dict()).get('description'))
                return numbers
            return None
        else:
            description: str = res.json().get("data", dict()).get("description")
            numbers = cls._get_phones(description)
            return numbers

    @classmethod
    def _get_phones(cls, description):
        numbers: list = re.findall("\d{10,12}", description)
        output = {"phones": list(), "mobiles": list()}
        for num in numbers:
            num = cls._convert_num_to_english(num)
            if num.startwith("09") or num.startwith("۰۹"):
                output['mobiles'].append(num)
            else:
                output['phones'].append(num)
        return output

    @staticmethod
    def _get_images(soup: BeautifulSoup):
        images_div = soup.find_all("div", class_="swiper-container")[0].find_all("img")
        images_list = list()
        for img in images_div:
            if img.attrs.get("src"):
                images_list.append(img.attrs.get("src"))
            elif img.attrs.get("data-srcset"):
                images_list.append(img.attrs.get("data-srcset"))
        return images_list

    @classmethod
    def fetch_detail_page_data(cls, urls) -> List[dict]:
        soups: List[BeautifulSoup] = cls._get_data_page(urls)
        output = list()
        for soup in soups:
            table_data: dict = cls._get_table_data(soup)
            car_brand: str = cls._get_car_brand(soup)
            description: str = cls._get_description(soup)
            images: list = cls._get_images(soup)
            dct = {
                "model": car_brand,
                "text": description,
                "images": images,
            }
            dct.update(table_data)
            output.append(dct)
        return output


class CaptchaSolver:

    @classmethod
    def solve_captcha(cls, image):
        image = cls._convert(image)
        # todo: 
        return

    @staticmethod
    def _convert(image_b64) -> np.array:
        image_data = image_b64.image_b64
        b = b64.b64decode(image_data)
        image = Image.open(io.BytesIO(b))
        image = np.array(image)
        return image
