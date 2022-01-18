from django.db import models

import pandas as pd

from typing import Union, List, Dict, Tuple, Iterable

from dart_fss.utils import dict_to_html, dataframe_astype
from dart_fss.fs import extract, FinancialStatement
from dart_fss.filings import search as se
from dart_fss.api.filings import get_corp_info


class Corp(models.Model):
    corp_code   = models.CharField(max_length=8, primary_key=True)
    corp_name   = models.CharField(max_length=256, null=True)

    def get_corp_info(self,):
        return get_corp_info(self.corp_code)
    def search_filings(self,
                       bgn_de: str = None,
                       end_de: str = None,
                       last_reprt_at: str = 'N',
                       pblntf_ty: Union[str, List[str], None] = None,
                       pblntf_detail_ty: Union[str, List[str], None] = None,
                       corp_cls: str = None,
                       sort: str = 'date',
                       sort_mth: str = 'desc',
                       page_no: int = 1,
                       page_count: int = 10):
        """공시보고서 검색

        Parameters
        ----------
        bgn_de: str, optional
            검색시작 접수일자(YYYYMMDD), 없으면 종료일(end_de)
        end_de: str, optional
            검색종료 접수일자(YYYYMMDD), 없으면 당일
        last_reprt_at: str, optional
            최종보고서만 검색여부(Y or N), default : N
        pblntf_ty: str, optional
            공시유형
        pblntf_detail_ty: str, optional
            공시상세유형
        corp_cls: str, optional
            법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타), 없으면 전체조회
        sort: str, optional
            정렬방법: '접수일자' date, '회사명' crp, '보고서명' rpt
        sort_mth: str, optional
            '오름차순' asc, '내림차순' desc, default : desc
        page_no: int, optional
            페이지 번호(1~n) default : 1
        page_count: int, optional
            페이지당 건수(1~100) 기본값 : 10, default : 100

        Returns
        -------
        SearchResults
            검색결과
        """
        return se(self.corp_code,
                  bgn_de=bgn_de,
                  end_de=end_de,
                  last_reprt_at=last_reprt_at,
                  pblntf_ty=pblntf_ty,
                  pblntf_detail_ty=pblntf_detail_ty,
                  corp_cls=corp_cls,
                  sort=sort,
                  sort_mth=sort_mth,
                  page_no=page_no,
                  page_count=page_count)


    def extract_fs(self,
                   bgn_de: str,
                   end_de: str = None,
                   fs_tp: Tuple[str] = ('bs', 'is', 'cis', 'cf'),
                   separate: bool = False,
                   report_tp: str = 'annual',
                   lang: str = 'ko',
                   separator: bool = True,
                   dataset: str = 'xbrl') -> FinancialStatement:
        """
         재무제표 검색

         Parameters
         ----------
         bgn_de: str
             검색 시작일자(YYYYMMDD)
         end_de: str, optional
             검색 종료일자(YYYYMMDD)
         fs_tp: tuple of str, optional
             'bs' 재무상태표, 'is' 손익계산서, 'cis' 포괄손익계산서, 'cf' 현금흐름표
         separate: bool, optional
             개별재무제표 여부
         report_tp: str, optional
             'annual' 1년, 'half' 반기, 'quarter' 분기
         lang: str, optional
             'ko' 한글, 'en' 영문
         separator: bool, optional
             1000단위 구분자 표시 여부
         dataset: str, optional
            'xbrl': xbrl 파일 우선 데이터 추출, 'web': web page 우선 데이터 추출(default: 'xbrl')
         Returns
         -------
         FinancialStatement
             제무제표 검색 결과

         """
        return extract(self.corp_code, bgn_de, end_de, fs_tp, separate, report_tp, lang, separator, dataset)