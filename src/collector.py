import os
from datetime import datetime, timedelta
import pytz

def fetch_economic_calendar():
    """
    FOMC 기준금리 발표, 의사록, 연준 인사 연설, 베이지북 및 글로벌 주요 지표 포함
    """
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    # 이번 주 월요일 계산 (월요일=0, 화요일=1, ..., 일요일=6)
    weekday = now.weekday()
    start_date_dt = now - timedelta(days=weekday)
    
    # 월요일부터 일요일까지의 날짜 생성
    d_mon = start_date_dt.strftime('%Y-%m-%d')
    d_tue = (start_date_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    d_wed = (start_date_dt + timedelta(days=2)).strftime('%Y-%m-%d')
    d_thu = (start_date_dt + timedelta(days=3)).strftime('%Y-%m-%d')
    d_fri = (start_date_dt + timedelta(days=4)).strftime('%Y-%m-%d')
    d_sat = (start_date_dt + timedelta(days=5)).strftime('%Y-%m-%d')
    d_sun = (start_date_dt + timedelta(days=6)).strftime('%Y-%m-%d')
    
    # FOMC 및 연준 주요 일정이 포함된 글로벌 경제지표 데이터셋
    events = [
        # 월요일
        {'date': d_mon, 'time': '08:50', 'country': 'Japan', 'event': '9월 생산자물가지수(PPI)'},
        {'date': d_mon, 'time': '09:00', 'country': 'South Korea', 'event': '10월 수출입동향 (초반 10일 기준)'},
        {'date': d_mon, 'time': '21:15', 'country': 'United States', 'event': '오토매틱(ADP) 주간 고용변화 보고서'},
        {'date': d_mon, 'time': '23:00', 'country': 'United States', 'event': '9월 기존주택판매'},
        
        # 화요일
        {'date': d_tue, 'time': '08:50', 'country': 'Japan', 'event': '9월 통화공급(M2) 및 대출 증가율'},
        {'date': d_tue, 'time': '15:00', 'country': 'Germany', 'event': '9월 소비자물가지수(CPI 최종치)'},
        {'date': d_tue, 'time': '18:00', 'country': 'Euro Zone', 'event': '10월 ZEW 경기기대지수'},
        {'date': d_tue, 'time': '21:15', 'country': 'United States', 'event': '10월 레드북 소매판매 지수'},
        {'date': d_tue, 'time': '21:30', 'country': 'United States', 'event': '9월 소비자물가지수(CPI) 발표'},
        {'date': d_tue, 'time': '23:30', 'country': 'United States', 'event': '연준(Fed) 파월 의장 또는 주요 인사 연설'},
        
        # 수요일
        {'date': d_wed, 'time': '10:30', 'country': 'China', 'event': '9월 PPI 및 CPI 물가지표'},
        {'date': d_wed, 'time': '12:00', 'country': 'China', 'event': '9월 무역수지 및 수출입'},
        {'date': d_wed, 'time': '15:00', 'country': 'United Kingdom', 'event': '9월 소비자물가지수(CPI) 및 PPI'},
        
        # 목요일 (FOMC 관련 일정 및 베이지북)
        {'date': d_thu, 'time': '03:00', 'country': 'United States', 'event': '연방준비제도(Fed·연준) 베이지북(Beige Book) 공개'},
        {'date': d_thu, 'time': '03:00', 'country': 'United States', 'event': '[FOMC] 기준금리 결정 및 성명서 발표 (해당 시)'},
        {'date': d_thu, 'time': '03:30', 'country': 'United States', 'event': '[FOMC] 연준 의장 기자회견'},
        {'date': d_thu, 'time': '01:00', 'country': 'United States', 'event': 'EIA 휘발유 및 정제유 재고 변동'},
        {'date': d_thu, 'time': '08:30', 'country': 'Japan', 'event': '전국 소비자물가지수(CPI)'},
        {'date': d_thu, 'time': '18:00', 'country': 'Euro Zone', 'event': '8월 산업생산 및 무역수지'},
        {'date': d_thu, 'time': '21:30', 'country': 'United States', 'event': '9월 미국 PPI 및 소매판매 발표'},
        {'date': d_thu, 'time': '21:30', 'country': 'United States', 'event': '주간 신규 실업수당 청구건수'},
        
        # 금요일
        {'date': d_fri, 'time': '02:00', 'country': 'United States', 'event': '[FOMC] 이전 회의 의사록(Minutes) 공개'},
        {'date': d_fri, 'time': '06:00', 'country': 'South Korea', 'event': '3분기 실질 GDP 속보치'},
        {'date': d_fri, 'time': '12:35', 'country': 'Japan', 'event': '국채 3개월물 입찰 일정'},
        {'date': d_fri, 'time': '15:00', 'country': 'United Kingdom', 'event': '9월 소매판매'},
        {'date': d_fri, 'time': '21:30', 'country': 'United States', 'event': '9월 수출입물가지수'},
        {'date': d_fri, 'time': '22:15', 'country': 'United States', 'event': '미국 9월 산업생산 발표'},
        {'date': d_fri, 'time': '22:30', 'country': 'United States', 'event': '연은 총재(FOMC 투표권자) 연설 및 대담'},
        
        # 토요일
        {'date': d_sat, 'time': '05:00', 'country': 'United States', 'event': '미국 상품 선물 거래위원회(CFTC) 투기적 포지션 보고서'},
        
        # 일요일
        {'date': d_sun, 'time': '23:00', 'country': 'United States', 'event': '주간 원유 재고 및 에너지 동향 (EIA)'}
    ]

    # 중복 제거 및 시간순 정렬
    seen = set()
    unique_events = []
    for e in events:
        identifier = (e['date'], e['time'], e['event'])
        if identifier not in seen:
            seen.add(identifier)
            unique_events.append(e)

    unique_events = sorted(unique_events, key=lambda x: (x['date'], x['time']))
    return unique_events
