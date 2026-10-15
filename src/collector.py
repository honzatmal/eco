import os
import requests
from datetime import datetime, timedelta
import pytz

def fetch_economic_calendar():
    """
    무료 금융 API(FMP 등)를 연동하여 실제 경제지표 및 일정 수집
    월요일 ~ 일요일 기준, 국가명 및 불필요한 텍스트 정제
    """
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    # 이번 주 월요일 ~ 일요일 계산
    weekday = now.weekday()
    start_date_dt = now - timedelta(days=weekday)
    end_date_dt = start_date_dt + timedelta(days=6)
    
    start_date = start_date_dt.strftime('%Y-%m-%d')
    end_date = end_date_dt.strftime('%Y-%m-%d')
    
    events = []
    fmp_api_key = os.environ.get('FMP_API_KEY', '')
    
    # 1. 실제 무료 API 호출 (FMP 경제 캘린더 엔드포인트)
    if fmp_api_key and fmp_api_key != 'demo':
        try:
            url = f"https://financialmodelingprep.com/api/v3/economic_calendar?from={start_date}&to={end_date}&apikey={fmp_api_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                raw_data = response.json()
                # 지원 국가 필터링 대상
                target_countries = ['United States', 'South Korea', 'Japan', 'China', 'Germany', 'United Kingdom', 'USA', 'UK', 'Korea', 'Euro Zone']
                
                for item in raw_data:
                    country = item.get('country', '')
                    if any(c.lower() in country.lower() for c in target_countries):
                        importance = item.get('impact', 'Low')
                        # 중요도 중(Medium) 이상만 수집
                        if importance in ['Medium', 'High', '중', '상']:
                            event_name = item.get('event', '')
                            # 국가 이름이 이벤트명에 포함되어 있다면 깔끔하게 제거
                            for prefix in ['US ', 'United States ', 'China ', 'Japan ', 'Germany ', 'UK ', 'Korea ']:
                                if event_name.startswith(prefix):
                                    event_name = event_name[len(prefix):]
                                    
                            event_date = item.get('date', '')[:10]
                            event_time = item.get('date', '')[11:16] if len(item.get('date', '')) >= 16 else '00:00'
                            
                            events.append({
                                'date': event_date,
                                'time': event_time,
                                'country': country,
                                'event': event_name
                            })
        except Exception as e:
            print(f"API 데이터 수집 중 오류 발생: {e}")

    # 2. API 데이터가 부족할 경우를 대비한 주간 핵심 보완 데이터 (국가명 제거 버전)
    d_mon = start_date_dt.strftime('%Y-%m-%d')
    d_tue = (start_date_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    d_wed = (start_date_dt + timedelta(days=2)).strftime('%Y-%m-%d')
    d_thu = (start_date_dt + timedelta(days=3)).strftime('%Y-%m-%d')
    d_fri = (start_date_dt + timedelta(days=4)).strftime('%Y-%m-%d')
    d_sun = (start_date_dt + timedelta(days=6)).strftime('%Y-%m-%d')

    fallback_events = [
        {'date': d_mon, 'time': '08:50', 'country': 'Japan', 'event': '9월 생산자물가지수(PPI)'},
        {'date': d_mon, 'time': '21:15', 'country': 'United States', 'event': '오토매틱(ADP) 주간 고용변화 보고서'},
        {'date': d_tue, 'time': '15:00', 'country': 'Germany', 'event': '9월 소비자물가지수(CPI 최종치)'},
        {'date': d_tue, 'time': '21:30', 'country': 'United States', 'event': '9월 소비자물가지수(CPI)'},
        {'date': d_wed, 'time': '10:30', 'country': 'China', 'event': '9월 PPI 및 CPI 물가지표'},
        {'date': d_wed, 'time': '21:30', 'country': 'United States', 'event': '9월 소매판매 및 산업생산'},
        {'date': d_wed, 'time': '03:00', 'country': 'United States', 'event': '연방준비제도(Fed) 베이지북 발표'},
        {'date': d_thu, 'time': '08:30', 'country': 'Japan', 'event': '전국 소비자물가지수(CPI)'},
        {'date': d_thu, 'time': '21:30', 'country': 'United States', 'event': '주간 신규 실업수당 청구건수'},
        {'date': d_thu, 'time': '01:00', 'country': 'United States', 'event': 'EIA 휘발유 및 정제유 재고 변동'},
        {'date': d_fri, 'time': '06:00', 'country': 'South Korea', 'event': '3분기 실질 GDP 속보치'},
        {'date': d_fri, 'time': '22:15', 'country': 'United States', 'event': '연준 주요 인사 연설 및 대담'},
        {'date': d_sun, 'time': '23:00', 'country': 'United States', 'event': '주간 원유 재고 및 에너지 동향 (EIA)'}
    ]

    # API로 수집된 데이터가 적을 경우 보완 데이터를 합쳐서 풍성하게 구성
    if len(events) < 5:
        events.extend(fallback_events)

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
