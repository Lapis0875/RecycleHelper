from datetime import date
import json
from typing import Any, Callable, Final, TYPE_CHECKING

from models.material import Material

if TYPE_CHECKING:
    from models.response import BarcodeResponse, ProductResponse
    from models.product import Product
    
BarcodeCrawlerFuncT = Callable[[Any, str], Material]


def parse_date(date_str: str) -> date | None:
    """
    20220929 형식의 문자열을 date 객체로 변한합니다.
    :param date_str: YYYYMMDD 형식의 문자열.
    :return: datetime.date 객체.
    """
    if len(date_str) != 8:
        return None
    year: int = int(date_str[:4])
    month: int = int(date_str[4:6])
    day: int = int(date_str[6:])
    return date(year, month, day)




class CachedBarcodeCrawler:
    def __init__(self, fn: BarcodeCrawlerFuncT, path: str = "./crawl_cache.json") -> None:
        self.path: str = path
        self.crawlerobj = None
        self.fn: BarcodeCrawlerFuncT = fn
        self.cache: dict[str, Material] = self.loadCache()
        self.openFn = open  # NameError: name 'open' is not defined / 올바른 타입힌트 모르겠어서 우선 패스.

    def loadCache(self) -> dict[str, Material]:
        """캐시 내용을 파일에서 다시 불러옵니다.

        Args:
            path (str): 파일의 경로.

        Returns:
            dict[str, Material]: 캐시 파일의 json 내용을 불러온 딕셔너리 객체.
        """
        try:
            with open(self.path, mode="rt", encoding="utf-8") as f:
                read: dict[str, int] = json.load(f)
                return {key: Material(value) for key, value in read.items()}
        except FileNotFoundError:
            return {}

    def saveCache(self):
        """캐시 내용을 파일에 저장합니다.

        Args:
            path (str): 파일의 경로.
            cache (dict[str, Material]): 캐시 파일의 json 내용을 불러온 딕셔너리 객체.
        """
        with self.openFn(self.path, mode="wt", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def __get__(self, owner, owner_cls):
        self.crawlerobj = owner
    
    def __call__(self, barcode: str) -> Material:
        res: Material | None = self.cache.get(barcode)
        if res is None:
            res = self.cache[barcode] = self.fn(self.crawlerobj, barcode)   # patch self.
        return res
    
    def __del__(self):
        self.saveCache()

def cacheIt(path: str = "./crawl_cache.json") -> Callable[[BarcodeCrawlerFuncT], BarcodeCrawlerFuncT]:
    """바코드로 제품 재질을 가져오는 함수에 사용하는 데코레이터로, 인자 값에 따른 캐싱을 제공합니다.

    Args:
        path (str, optional): 캐시 내용을 저장할 파일 경로입니다. 기본 값은 "./crawl_cache.json" 입니다.

    Returns:
        Callable[[BarcodeCrawlerFuncT], BarcodeCrawlerFuncT]: 바코드로 제품 재질을 가져오는 함수의 데코레이터입니다.
    """
    def deco(fn: BarcodeCrawlerFuncT) -> BarcodeCrawlerFuncT:
        """바코드로 제품 재질을 가져오는 함수에 사용하는 데코레이터로, 인자 값에 따른 캐싱을 제공합니다.

        Args:
            fn (BarcodeCrawlerFuncT): 바코드로 제품 재질을 가져오는 함수의 원형입니다.

        Returns:
            BarcodeCrawlerFuncT: 데코레이팅 된 함수입니다.
        """
        return CachedBarcodeCrawler(fn)
    return deco