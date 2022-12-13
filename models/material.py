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


CountMap: dict[str, Material] = {
    "CAN": Material.CAN,
    "금속": Material.CAN,
    "캔": Material.CAN,
    "PET": Material.PLASTIC,
    "PVC": Material.PLASTIC,
    "PE": Material.PLASTIC,
    "PP": Material.PLASTIC,
    "PS": Material.PLASTIC,
    "PSP": Material.PLASTIC,
}   # 최우선 재질을 결정하기 위한, 재질 표기별 재질 분류를 매핑으로 정리.



def parseMaterial(materialText: str) -> Material:
    """재질 표기를 분석해, 가장 구성 요소가 많은 1순위 재질 분류를 추려 반환합니다.

    Args:
        materialText (str): 재질 표기 텍스트.

    Returns:
        Material: 1순위 재질 분류.
    """
    counter: dict[Material, int] = {m: 0 for m in Material}
    for check in CountMap:
        if check in materialText:
            counter[CountMap[check]] += 1
    mat: Material = max(counter.keys(), key=lambda k: counter[k])
    return mat