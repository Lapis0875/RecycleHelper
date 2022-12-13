from dataclasses import dataclass

from models.material import Material
from models.response import BarcodeResponse, ProductResponse


@dataclass(slots=True, frozen=True)
class Product:
    """
    최종 제품 정보를 담을 데이터 클래스.
    """
    barcode: str                # 바코드 번호
    material: Material          # 포장재질
    prdlst_report_no: int      # 품목제조번호
    prdlst_nm: str             # 제품명
    rawmtrl_nm: str             # 품목유형(기능지표성분)
