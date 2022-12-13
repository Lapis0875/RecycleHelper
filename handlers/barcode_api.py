from os import environ
from pprint import pprint
import re
from typing import cast, Final

import requests
from playwright.sync_api import sync_playwright, Playwright, Browser, Page, Locator
from playwright.sync_api._context_manager import PlaywrightContextManager

from models.material import parseMaterial, Material
from models.response import ProductResponse
from utils import cacheIt

prdNoPattern = re.compile(r"(?:(\d{14})+[\w_, \(\)]{0,})+")


class BarcodeHandler:
    def __init__(self):
        self.session: requests.Session = requests.Session()
        self.__key: Final[str] = environ["FOOD_SAFETY_KR_API_KEY"]
        self.playwright: Playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch()

    def teardown(self):
        """
        teardown
        """
        if self.session is not None:
            self.session.close()
        self.playwright.stop()

    @cacheIt()
    def search(self, barcode: str) -> Material:
        """바코드에 해당하는 제품 정보를 크롤링 해옵니다.

        Args:
            barcode (str): 바코드 번호 값.

        Returns:
            Material : 제품의 포장 재질에 대응하는 Material 객체.
        """
        # init
        prdReportNo: str | None = self.getPrdReportNo(barcode)
        if prdReportNo is None:
            raise ValueError("바코드 번호에 해당하는 상품을 찾을 수 없습니다.")
        material: Material | None = self.product_search(prdReportNo)
        if material is None:
            raise ValueError("품목보고번호에 해당하는 상품을 찾을 수 없습니다.")
        return material
    
    def getPrdReportNo(self, barcode: str) -> str | None:
        """바코드 번호를 사용해 품목 보고 번호를 얻습니다. 유통상품지식뱅크를 크롤링합니다.

        Args:
            browser (Browser): Playwright의 브라우저 객체.
            barcode (str): 바코드 번호 값.

        Returns:
            str | None: 품목 보고 번호. 없을 경우 None, 있을 경우 품목 보고 번호의 문자열
        """
        page: Page = self.browser.new_page()
        page.goto("http://www.allproductkorea.or.kr/products/search")
        
        # search
        searchElem: Locator = page.locator(selector=".header_searchV2")
        searchElem.locator(selector="#searchText").fill(barcode)
        searchElem.locator(selector="button").click()
        
        # get result
        items: Locator = page.locator(selector=".spl_list")
        items.click()
        prdReportNoLoc: Locator = page.locator(selector="body > div.sub_content2 > div > div.pdv_korcharDetail > div.pdv_wrap_korcham > table > tbody > tr:nth-child(10) > td")
        prdReportNoStr = prdReportNoLoc.inner_text()
        print(prdReportNoStr)
        mat: re.Match | None = prdNoPattern.match(prdReportNoStr)
        
        prdReporNo: str | None = None
        if (mat is not None):
            grp = mat.groups()
            pprint(grp)
            prdReporNo = grp[0]
        
        return prdReporNo

    def product_search(self, prdReportNo: str) -> Material | None:
        url: str = f"http://openapi.foodsafetykorea.go.kr/api/{self.__key}/I0030/json/1/5/"\
                   f"PRDLST_REPORT_NO={prdReportNo}"
                   # f"&BSSH_NM={barcode_resp.bssh_nm}"\
                   # f"&PRDLST_NM={barcode_resp.prdlst_nm}"\
        print(f"품목보고번호 사용해 제품 정보 조회 -> {url}")
        with self.session.get(url) as resp:
            json = resp.json()
            pprint(json)
            if json["I0030"]["RESULT"]["CODE"] == "INFO-200":
                return None   # 결과 없음
            wrapped: list[ProductResponse] = [ProductResponse.from_json(**r) for r in json["I0030"]["row"]]
            return parseMaterial(wrapped[0].frmlc_mtrqlt)

    def __del__(self):
        self.teardown()