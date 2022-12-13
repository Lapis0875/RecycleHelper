from typing import Final
from os import environ

import serial
import serial.tools.list_ports

import bluetooth

from handlers.barcode_api import BarcodeHandler
from handlers.bluetooth_handler import BluetoothHandler, Module

from models.material import Material
from models.response import BarcodeResponse, ProductResponse
from models.product import Product

PORT: Final[str] = "/dev/ttyUSB0"
BAUDRATE: Final[int] = 9600
environ["FOOD_SAFETY_KR_API_KEY"] = "5c3691cdc5fb4104bc46"

def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print(f"{bluetooth.lookup_name(bdaddr)}[{bdaddr}]")

class BluetoothTester:
    def __init__(self):
        # lookUpNearbyBluetoothDevices()
        print([str(port) for port, desc, hwid in serial.tools.list_ports.comports()])
        self.bluetooth_handler = BluetoothHandler()
    
    def run(self):
        test_module1: Module = Module("/dev/rfcomm0")
        test_module2: Module = Module("/dev/rfcomm1")

        print("Connecting devices...")
        self.bluetooth_handler.connect(Material.NORMAL, test_module1)
        self.bluetooth_handler.connect(Material.GLASS, test_module2)
        self.bluetooth_handler.pair(Material.NORMAL)
        self.bluetooth_handler.pair(Material.GLASS)
        from time import sleep
        sleep(10)
        print("Calling devices...")
        self.bluetooth_handler.call(Material.NORMAL)
        self.bluetooth_handler.call(Material.GLASS)


class BarcodeSearcher:
    """
    바코드 번호를 사용해, 식품의약처 API로 제품의 포장 재질을 알아냅니다.
    """
    def __init__(self):
        self.serial: serial.Serial = serial.Serial(PORT, BAUDRATE)  # 
        self.barcode_api = BarcodeHandler()
        self.bluetooth_handler = BluetoothHandler()

    def run(self):
        """
        서비스 가동.
        """
        running: bool = True
        while running:
            line: bytes = self.serial.readline()   # 타임아웃을 지정하지 않았으므로, 시리얼로부터 완전한 한 줄 (바코드 번호 전체)를 받을때까지 대기.
            data: str = line.decode("utf-8").strip()   # 바이트열을 문자열로 변환하고, 불필요한 공백을 제거.
            header, body = data.split(":")
            match header:
                case "bc":
                    # 바코드 입력
                    self.barcodeTask(body)
                case "bt":
                    # 블루투스 명령
                    self.bluetoothConnectionTask(body)
            
        self.teardown()

    def teardown(self):
        """
        서비스 종료시 필요한 처리 핸들링.
        """
        self.serial.close()
        self.barcode_api.teardown()

    def barcodeTask(self, body: str) -> None:
        if not body.isdigit() or len(body) != 13:
            return
        try:
            mat: Material = self.barcode_api.search(body)
            self.bluetooth_handler.call(mat)
        except ValueError:
            # 조회 불가한 제품에 대한 처리.
            return

    def bluetoothConnectionTask(self, body: str) -> None:
        material = Material(int(body))
        return self.bluetooth_handler.pair(material)
