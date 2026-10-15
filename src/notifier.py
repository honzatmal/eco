import os
import requests
from datetime import datetime, timedelta

def send_telegram_message(message):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        raise ValueError("Telegram Bot Token 또는 Chat ID가 설정되지 않았습니다.")
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"텔레그램 전송 실패: {response.text}")
    print("텔레그램 메시지 전송 성공!")

def get_country_flag(country_name):
    """국가 이름에 맞는 국기 이모지 반환"""
    country_lower = country_name.lower()
    if 'united states' in country_lower or 'usa' in country_lower or '미국' in country_lower:
        return "🇺🇸"
    elif 'south korea' in country_lower or 'korea' in country_lower or '한국' in country_lower:
        return "🇰🇷"
    elif 'japan' in country_lower or '일본' in country_lower:
        return "🇯🇵"
    elif 'china' in country_lower or '중국' in country_lower:
        return "🇨🇳"
    elif 'germany' in country_lower or '독일' in country_lower:
        return "🇩🇪"
    elif 'united kingdom' in country_lower or 'uk' in country_lower or '영국' in country_lower:
        return "🇬🇧"
    elif 'euro' in country_lower or '유로' in country_lower:
        return "🇪🇺"
    return "🌐"

def format_report(events):
    # 날짜 범위 계산 (이번 주 월요일 ~ 금요일/일요일 등)
    now = datetime.now()
    start_date_str = now.strftime('%m월 %d일')
    end_date_str = (now + timedelta(days=6)).strftime('%m월 %d일')
    
    report = f"🔥 *{start_date_str}~{end_date_str} 주요 경제지표 및 연설일정*\n\n"
    
    if not events:
        report += "이번 주 발표되는 주요 경제지표가 없습니다.\n"
        return report
        
    # 날짜별로 이벤트 그룹화
    grouped_events = {}
    for e in events:
        date_key = e.get('date', '기타')
        if date_key not in grouped_events:
            grouped_events[date_key] = []
        grouped_events[date_key].append(e)
        
    # 요일 한글 변환 맵
    weekday_map = {
        0: '월요일', 1: '화요일', 2: '수요일', 
        3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'
    }
    
    for date_str, date_events in sorted(grouped_events.items()):
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            m_d_str = f"{dt.month}월 {dt.day}일"
            weekday_str = weekday_map[dt.weekday()]
            day_header = f"✅ *{m_d_str} {weekday_str}*"
        except:
            day_header = f"✅ *{date_str}*"
            
        report += f"{day_header}\n"
        
        for e in date_events:
            time_str = e.get('time', '')
            # 시간 포맷이 HH:MM 형태라면 그대로 사용
            if len(time_str) >= 5:
                time_display = time_str[:5]
            else:
                time_display = "종일"
                
            country = e.get('country', '')
            flag = get_country_flag(country)
            event_name = e.get('event', '')
            
            # 이미지 스타일의 깔끔한 한 줄 포맷 (시간 + 국기 + 이벤트명)
            report += f"{time_display} {flag} {event_name}\n"
            
            # 상세형 정보 (예측치/이전치 및 금 매매 영향 참고 추가)
            forecast = e.get('forecast', '발표전')
            previous = e.get('previous', '-')
            
            # 금 매매 영향 간단 요약
            gold_tip = "중립"
            ev_lower = event_name.lower()
            if 'cpi' in ev_lower or '인플레이션' in ev_lower or 'ppi' in ev_lower:
                gold_tip = "물가 지표 연동 변동성 주의"
            elif 'fomc' in ev_lower or '금리' in ev_lower or '연준' in ev_lower:
                gold_tip = "통화정책 결정 (금 가격 큰 영향)"
            elif '원유' in ev_lower or 'eia' in ev_lower:
                gold_tip = "원유 재고 연동"
                
            report += f"   └ 📊 예측: {forecast} | 이전: {previous} | 🥇 {gold_tip}\n"
            
        report += "\n"
        
    return report
