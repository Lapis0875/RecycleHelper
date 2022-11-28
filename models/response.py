from dataclasses import dataclass
from datetime import date

from utils import parse_date


@dataclass(slots=True, frozen=True)
class BarcodeResponse:
    """
    바코드 연계 제품 정보 API를 활용해 얻은 응답 정보를 래핑합니다.
    """
    bar_cd: str             # 유통 바코드
    bssh_nm: str            # 제조사명
    clsbiz_dt: date | None          # 폐업일자
    prdlst_report_no: int  # 품목보고(신고)번호
    prms_dt: date       # 보고(신고일)
    end_dt: date | None        # 생산중단일
    prdlst_nm: str         # 제품명
    pog_daycnt: str         # 유통/소비 기한
    prdlst_dcnm: str       # 식품 유형
    induty_nm: str          # 업종
    site_addr: str          # 주소

    @classmethod
    def from_json(
            cls,
            PRDLST_REPORT_NO: str,
            PRMS_DT: str,
            END_DT: str,
            PRDLST_NM: str,
            POG_DAYCNT: str,
            PRDLST_DCNM: str,
            BSSH_NM: str,
            INDUTY_NM: str,
            SITE_ADDR: str,
            CLSBIZ_DT: str,
            BAR_CD: str
    ) -> "BarcodeResponse":
        return cls(
            prdlst_report_no=int(PRDLST_REPORT_NO),
            prms_dt=parse_date(PRMS_DT),
            end_dt=parse_date(END_DT),
            prdlst_nm=PRDLST_NM,
            pog_daycnt=POG_DAYCNT,
            prdlst_dcnm=PRDLST_DCNM,
            bssh_nm=BSSH_NM,
            induty_nm=INDUTY_NM,
            site_addr=SITE_ADDR,
            clsbiz_dt=parse_date(CLSBIZ_DT),
            bar_cd=BAR_CD
        )


@dataclass(slots=True, frozen=True)
class ProductResponse:
    """
    건강기능식품 품목제조 신고사항 API를 활용해 얻은 응답 정보를 래핑합니다.
    """
    lcns_no: str                # 인허가번호
    bssh_nm: str                # 업소명
    prdlst_report_no: int       # 품목제조번호
    prdlst_nm: str              # 제품명
    prms_dt: date               # 보고(신고일)
    pog_daycnt: str             # 유통/소비 기한
    dispos: str                 # 성상
    ntk_mthd: str               # 섭취방법
    primary_fnclty: str         # 주된기능성
    iftkn_atnt_matr_cn: str     # 섭취시 주의사항
    cstdy_mthd: str             # 보관방법
    prdlst_cdnm: str            # 식품 유형
    stdr_stnd: str              # 기준규격
    hieng_lntrt_dvs_nm: str     # 고열량 저영양 여부
    production: str             # 생산 종료 여부
    child_crtfc_yn: str         # 어린이기호식품품질인증여부
    prdt_shap_cd_nm: str        # 제품형태
    frmlc_mtrqlt: str           # 포장재질
    rawmtrl_nm: str             # 품목유형(기능지표성분)
    induty_cd_nm: str           # 업종
    last_updt_dtm: str          # 최종수정일자
    indiv_rawmtrl_nm: str       # 기능성 원재료
    etc_rawmtrl_nm: str         # 기타 원재료
    cap_rawmtrl_nm: str         # 캡슐 원재료

    @classmethod
    def from_json(
            cls,
            LCNS_NO: str,
            BSSH_NM: str,
            PRDLST_REPORT_NO: str,
            PRDLST_NM: str,
            PRMS_DT: str,
            POG_DAYCNT: str,
            DISPOS: str,
            NTK_MTHD: str,
            PRIMARY_FNCLTY: str,
            IFTKN_ATNT_MATR_CN: str,
            CSTDY_MTHD: str,
            PRDLST_CDNM: str,
            STDR_STND: str,
            HIENG_LNTRT_DVS_NM: str,
            PRODUCTION: str,
            CHILD_CRTFC_YN: str,
            PRDT_SHAP_CD_NM: str,
            FRMLC_MTRQLT: str,
            RAWMTRL_NM: str,
            INDUTY_CD_NM: str,
            LAST_UPDT_DTM: str,
            INDIV_RAWMTRL_NM: str,
            ETC_RAWMTRL_NM: str,
            CAP_RAWMTRL_NM: str
    ) -> "ProductResponse":
        return cls(
            LCNS_NO,
            BSSH_NM,
            int(PRDLST_REPORT_NO),
            PRDLST_NM,
            parse_date(PRMS_DT),
            POG_DAYCNT,
            DISPOS,
            NTK_MTHD,
            PRIMARY_FNCLTY,
            IFTKN_ATNT_MATR_CN,
            CSTDY_MTHD,
            PRDLST_CDNM,
            STDR_STND,
            HIENG_LNTRT_DVS_NM,
            PRODUCTION,
            CHILD_CRTFC_YN,
            PRDT_SHAP_CD_NM,
            FRMLC_MTRQLT,
            RAWMTRL_NM,
            INDUTY_CD_NM,
            LAST_UPDT_DTM,
            INDIV_RAWMTRL_NM,
            ETC_RAWMTRL_NM,
            CAP_RAWMTRL_NM
        )