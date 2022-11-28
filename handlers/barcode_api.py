from os import environ
from pprint import pprint
from typing import Final

import requests

from models.product import Product
from models.response import BarcodeResponse, ProductResponse
from utils import parse_product


class BarcodeHandler:
    def __init__(self):
        self.session: requests.Session | None = None
        self.__key: Final[str] = environ["FOOD_SAFETY_KR_API_KEY"]

    def setup(self):
        self.session = requests.Session()

    def teardown(self):
        self.session.close()
        self.session = None

    def search(self, barcode: str) -> Product | None:
        """
        바코드 번호를 받아, 제품 정보를 조회한다.
        :param barcode: 바코드 번호.
        :return: 래핑된 제품 객체.
        """
        barcode_resps: list[BarcodeResponse] = self.barcode_search(barcode)
        pprint(barcode_resps)
        if len(barcode_resps) == 0:
            return None
        product_resps: list[ProductResponse] = self.product_search(barcode_resps[0])
        pprint(product_resps)
        if len(product_resps) == 0:
            return None
        return parse_product(barcode_resps[0], product_resps[0])

    def barcode_search(self, barcode: str) -> list[BarcodeResponse]:
        with self.session.get(
                f"http://openapi.foodsafetykorea.go.kr/api/{self.__key}/C005/json/1/5/BAR_CD={barcode}"
        ) as resp:
            json = resp.json()
            pprint(json)
            if json["C005"]["RESULT"]["CODE"] == "INFO-200":
                return []   # 결과 없음
            wrapped: list[BarcodeResponse] = [BarcodeResponse.from_json(**r) for r in json["C005"]["row"]]
            return wrapped

    def product_search(self, barcode_resp: BarcodeResponse) -> list[ProductResponse]:
        url: str = f"http://openapi.foodsafetykorea.go.kr/api/{self.__key}/I0030/json/1/5/"\
                   f"PRDLST_REPORT_NO={barcode_resp.prdlst_report_no}"
                   # f"&BSSH_NM={barcode_resp.bssh_nm}"\
                   # f"&PRDLST_NM={barcode_resp.prdlst_nm}"\
        print(url)
        with self.session.get(url) as resp:
            json = resp.json()
            pprint(json)
            if json["I0030"]["RESULT"]["CODE"] == "INFO-200":
                return []   # 결과 없음
            wrapped: list[ProductResponse] = [ProductResponse.from_json(**r) for r in json["I0030"]["row"]]
            return wrapped
