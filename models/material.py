from enum import IntEnum


class Material(IntEnum):
    """
    포장재질 (분리수거용 enum)
    """
    NORMAL = 0
    PAPER = 1
    PLASTIC = 2
    CAN = 3
    GLASS = BOTTLES = 4
    STYROFOAM = 5   # 스티로폼/완충제
    VINYLS = FILMS = 6
    SCRAP = 7
    CLOTH = 8
