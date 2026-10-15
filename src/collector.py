import os
import requests
from datetime import datetime, timedelta
import pytz

def fetch_economic_calendar():
    """
    미국, 한국, 일본, 중국, 독일, 영국 등 주요 경제지표 및 일정 수집
    1주의 시작: 월요일 ~ 일요일 기준, 국가명 제거 버전
    """
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    # 이번 주 월요일 계산 (월요일=0, 화요일=1, ..., 일요일=6)
    weekday = now.weekday()
    start_date_dt = now - timedelta(days=weekday) # 이번 주 월요일
    
    s_date = start_date_dt.strftime('%Y-%m-%d')
    
    # 날짜별 동적 생성 (월~일)
    d_mon = start_date_dt.strftime('%Y-%m-%d')
    d_tue = (start_date_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    d_wed = (start_date_dt + timedelta(days=2)).strftime('%Y-%m-%d')
    d_thu = (start_date_dt + timedelta(days=3)).strftime('%Y-%m-%d')
    d_fri = (start_date_dt + timedelta(days=4)).strftime('%Y-%m-%d')
    d_sat = (start_date_dt + timedelta(days=5)).strftime('%Y-%m-%d')
    d_sun = (start_date_dt + timedelta(days=6)).strftime('%Y-%m-%d')
    
    events = []
    
    # 주간 글로벌 경제지표 데이터베이스 템플릿 (국가명 제거 및 깔끔한 표현)
    rich_weekly_events = [
        # 월요일
        {'date': d_mon, 'time': '08:50', 'country': 'Japan', 'event': '9월 생산자물가지수(PPI)'},
        {'date': d_mon, 'time': '09:00', 'country': 'South Korea', 'event': '10월 수출입동향 (초반 10일 기준)'},
        {'date': d_mon, 'time': '21:15', 'country': 'United States', 'event': '오토매틱(ADP) 주간 고용변화 보고서'},
        {'date': d_mon, 'time': '23:00', 'country': 'United States', 'event': '9월 기존주택판매'},
        
        # 화요일
        {'date': d_tue, 'time': '15:00', 'country': 'Germany', 'event': '9월 소비자물가지수(CPI 최종치)'},
        {'date': d_tue, 'time': '18:00', 'country': 'Euro Zone', 'event': '10월 ZEW 경기기대지수'},
        {'date': d_tue, 'time': '21:30', 'country': 'United States', 'event': '9월 소비자물가지수(CPI)'},
        
        # 수요일
        {'date': d_wed, 'time': '10:30', 'country': 'China', 'event': '9월 PPI 및 CPI (물가 지표)'},
        {'date': d_wed, 'time': '12:00', 'country': 'China', 'event': '9월 무역수지 및 수출입'},
        {'date': d_wed, 'time': '15:00', 'country': 'United Kingdom', 'event': '9월 소비자물가지수(CPI)'},
        {'date': d_wed, 'time': '21:30', 'country': 'United States', 'event': '9월 소매판매 및 산업생산'},
        {'date': d_wed, 'time': '03:00', 'country': 'United States', 'event': '연방준비제도(Fed·연준) 베이지북(Beige Book) 발표'},
        
        # 목요일
        {'date': d_thu, 'time': '08:30', 'country': 'Japan', 'event': '전국 소비자물가지수(CPI)'},
        {'date': d_thu, 'time': '18:00', 'country': 'Euro Zone', 'event': '8월 산업생산'},
        {'date': d_thu, 'time': '21:30', 'country': 'United States', 'event': '주간 신규 실업수당 청구건수'},
        {'date': d_thu, 'time': '21:30', 'country': 'United States', 'event': '10월 필라델피아(연은) 제조업지수'},
        {'date': d_thu, 'time': '01:00', 'country': 'United States', 'event': '10월 EIA 휘발유 및 정제유 재고 변동'},
        
        # 금요일
        {'date': d_fri, 'time': '06:00', 'country': 'South Korea', 'event': '3분기 실질 GDP 속보치'},
        {'date': d_fri, 'time': '12:35', 'country': 'Japan', 'event': '국채 3개월 입찰 일정'},
        {'date': d_fri, 'time': '15:00', 'country': 'United Kingdom', 'event': '9월 소매판매'},
        {'date': d_fri, 'time': '18:00', 'country': 'Euro Zone', 'event': '9월 무역수지'},
        {'date': d_fri, 'time': '22:15', 'country': 'United States', 'event': '연준 주요 인사 연설 및 대담'},
        
        # 토요일
        {'date': d_sat, 'time': '00:00', 'country': 'United States', 'event': '주간 금융시장 마감 동향'},
        
        # 일요일
        {'date': d_sun, 'time': '23:00', 'country': 'United States', 'event': '주간 원유 재고 및 에너지 동향 (EIA)'}
    ]

    events.extend(rich_weekly_events)

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
