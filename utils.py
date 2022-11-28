from datetime import date
from typing import Final, TYPE_CHECKING

from models.material import Material

if TYPE_CHECKING:
    from models.response import BarcodeResponse, ProductResponse
    from models.product import Product


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


MATERIAL_MAP: Final[dict[str, Material]] = {
    "PTP": Material.PLASTIC,
    "HDPE": Material.PLASTIC,
    "PE": Material.PLASTIC,
    "PET": Material.PLASTIC,

}


def get_materials(frmlc_mtrqlt: str) -> list[Material]:
    """
    제품의 포장 재질을 목록으로 반환합니다. 우선순위에 따라 순서를 정렬합니다.
    example:
    "PTP(염화비닐수지+알루미늄호일), HDPE(고밀도폴리에틸렌), PE(폴리에틸렌), PET(폴리에틸렌테레프탈레이트), PP(폴리프로필렌), PS(폴리스틸렌), 유리, AL(알루미늄), 철."

    :param frmlc_mtrqlt: 제품의 포장 재질을 표현하는 문자열입니다.
    :return: 포장 재질의 list입니다.
    """
    mapped: dict[Material, int] = {mat: 0 for mat in Material}
    sliced: list[str] = frmlc_mtrqlt.split(", ")
    for s in sliced:
        for key in MATERIAL_MAP:
            if s.startswith(key):
                mapped[MATERIAL_MAP[key]] += 1

    res: list[Material] = sorted(filter(lambda m: mapped[m] > 0, Material), key=lambda m: mapped[m])
    return res


def parse_product(barcode_resp: "BarcodeResponse", product_resp: "ProductResponse") -> "Product":
    """
    제품 정보를 포함하는 Product 객체를 생성합니다.
    :param barcode_resp: 바코드 api로부터의 응답입니다.
    :param product_resp: 제품 상세정보 api로부터의 응답입니다.
    :return: 정보를 포함하는 Product 객체입니다.
    """

    return Product(
        barcode_resp.bar_cd,
        get_materials(product_resp.frmlc_mtrqlt),
        product_resp.prdlst_report_no,
        product_resp.prdlst_nm,
        product_resp.rawmtrl_nm
    )