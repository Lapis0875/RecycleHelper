from typing import Final
from os import environ

import serial

from handlers.barcode_api import BarcodeHandler
from handlers.bluetooth_handler import BluetoothHandler
from models.response import BarcodeResponse, ProductResponse
from models.product import Product

PORT: Final[str] = "/dev/ttyUSB0"
BAUDRATE: Final[int] = 9600
environ["FOOD_SAFETY_KR_API_KEY"] = "5c3691cdc5fb4104bc46"


class BarcodeTester:
    def __init__(self):
        self.barcode_api = BarcodeHandler()

    def run(self):
        """
        서비스 가동.
        """
        self.setup()
        self.loop()
        self.teardown()

    def setup(self):
        """
        실행 준비 단계.
        """
        self.barcode_api.setup()

    def loop(self):
        """
        아두이노의 loop()와 함께 동작하며 주요 로직을 처리함.
        """
        barcodes: dict[str, str] = {
            "매일맛있는진간장골드": "8801791000055",
            "엄가선콩메주된장": "8801791797726",
            "TAMS 제로 오렌지향": "8801056229290",
            "크리넥스 여행용 티슈": "8801166021319",
            "케이메딕 마스크": "8809731680039"
        }
        for name, b in barcodes.items():
            print(f"{name}[{b}] 테스트.")
            product: Product = self.search(b)
            print(product, end="\n\n")

    def teardown(self):
        """
        서비스 종료시 필요한 처리 핸들링.
        """
        self.barcode_api.teardown()

    def search(self, barcode: str) -> Product:
        return self.barcode_api.search(barcode)

    def barcode_search(self, barcode: str) -> list[BarcodeResponse]:
        return self.barcode_api.barcode_search(barcode)

    def product_search(self, barcode_resp: BarcodeResponse) -> list[ProductResponse]:
        return self.barcode_api.product_search(barcode_resp)


class BarcodeSearcher:
    """
    바코드 번호를 사용해, 식품의약처 API로 제품의 포장 재질을 알아냅니다.
    """
    def __init__(self):
        self.serial: serial.Serial = serial.Serial(PORT, BAUDRATE)
        self.barcode_api = BarcodeHandler()
        self.bluetooth_handler = BluetoothHandler()

    def run(self):
        """
        서비스 가동.
        """
        self.setup()
        self.loop()
        self.teardown()

    def setup(self):
        """
        실행 준비 단계.
        """
        self.barcode_api.setup()
        self.bluetooth_handler.setup()

    def loop(self):
        """
        아두이노의 loop()와 함께 동작하며 주요 로직을 처리함.
        """
        running: bool = True
        while running:
            line: bytes = self.serial.readline()   # 타임아웃을 지정하지 않았으므로, 시리얼로부터 완전한 한 줄 (바코드 번호 전체)를 받을때까지 대기.
            if line == b"exit\r\n":
                break
            barcode: str = line.decode("utf-8").strip()   # 바이트열을 문자열로 변환하고, 불필요한 공백을 제거.
            product = self.search(barcode)
            # TODO : 블루투스 연결
            self.serial.write(product.material.value.encode("utf-8"))   # 아두이노로 바코드 번호를 전송.

    def teardown(self):
        """
        서비스 종료시 필요한 처리 핸들링.
        """
        self.serial.close()
        self.bluetooth_handler.teardown()
        self.barcode_api.teardown()

    def search(self, barcode: str) -> Product:
        return self.barcode_api.search(barcode)

    def barcode_search(self, barcode: str) -> list[BarcodeResponse]:
        return self.barcode_api.barcode_search(barcode)

    def product_search(self, barcode_resp: BarcodeResponse) -> list[ProductResponse]:
        return self.barcode_api.product_search(barcode_resp)
