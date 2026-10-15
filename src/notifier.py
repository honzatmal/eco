import os
import requests
from datetime import datetime, timedelta
import pytz

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
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    weekday = now.weekday()
    start_date_dt = now - timedelta(days=weekday) # 이번 주 월요일
    end_date_dt = start_date_dt + timedelta(days=6)   # 이번 주 일요일
    
    start_date_str = f"{start_date_dt.month}월 {start_date_dt.day}일"
    end_date_str = f"{end_date_dt.month}월 {end_date_dt.day}일"
    
    report = f"🔥 *{start_date_str}~{end_date_str} 주요 경제지표 및 연설일정 (월~일)*\n\n"
    
    if not events:
        report += "이번 주 발표되는 주요 경제지표가 없습니다.\n"
        return report
        
    grouped_events = {}
    for e in events:
        date_key = e.get('date', '기타')
        if date_key not in grouped_events:
            grouped_events[date_key] = []
        grouped_events[date_key].append(e)
        
    # 요일 순서 (월요일부터 일요일까지)
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
            time_display = time_str[:5] if len(time_str) >= 5 else "종일"
                
            country = e.get('country', '')
            flag = get_country_flag(country)
            event_name = e.get('event', '')
            
            # 국가 이름 없이 국기와 시간, 이벤트명만 깔끔하게 출력
            report += f"{time_display} {flag} {event_name}\n"
            
        report += "\n"
        
    return report
