from models.material import Material


class ChangongBluetoothException(Exception):
    """
    블루투스 관련 오류의 부모 클래스
    """
    msg: str

    def __init__(self, msg: str):
        self.msg = msg


class NotConnectedException(ChangongBluetoothException):
    """
    아직 연결되지 않은 항목의 기기를 연결 해지하려 할 시 오류를 발생시킵니다.
    """
    mat: Material

    def __init__(self, mat: Material):
        self.mat = mat
        super().__init__(f"이미 연결된 {mat.name}에 추가로 기기를 연결할 수 없습니다.")


class AlreadyConnectedException(ChangongBluetoothException):
    """
    이미 연결된 항목에 새 기기를 추가로 연결하려 할 시 오류를 발생시킵니다.
    """
    mat: Material

    def __init__(self, mat: Material):
        self.mat = mat
        super().__init__(f"이미 연결된 {mat.name}에 추가로 기기를 연결할 수 없습니다.")


class Module:
    material: Material
    def __init__(self, material: Material) -> None:
        self.material = material
    
    def call(self):
        """
        블루투스 통신 처리.
        """
        pass


class BluetoothHandler:
    """
    블루투스 모듈 연결 관리
    """
    def __init__(self) -> None:
        self.devices: dict[Material, Module | None] = {
            mat: None
            for mat in Material
        }

    def connect(self, mat: Material, mod: Module):
        if self.devices[mat] is not None:
            raise AlreadyConnectedException(mat)
        self.devices[mat] = mod
    
    def disconnect(self, mat: Material):
        if self.devices[mat] is None:
            raise NotConnectedException(mat)
        self.devices[mat] = None

    def call(self, mat: Material):
        device: Module = self.devices[mat]
        # device.write(...)
