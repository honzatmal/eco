import os
import requests

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

def format_report(events):
    report = "📊 *[주간 주요 경제지표 및 일정 리포트]*\n"
    report += "대상 국가: 미국, 한국, 일본, 중국, 독일, 영국\n"
    report += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not events:
        report += "이번 주 발표되는 주요 중·상 중요도 경제지표가 없습니다.\n"
        return report
        
    for idx, e in enumerate(events, 1):
        # 금 매매 영향 참고 가이드 분석 (예시 로직)
        gold_impact = "중립 / 시장 변동성 주시"
        event_name = e['event'].lower()
        if 'cpi' in event_name or '인플레이션' in event_name or 'ppi' in event_name:
            gold_impact = "물가 상승 시 금 가격 하락 압력(금리 인상 우려), 하락 시 금 상승"
        elif 'fomc' in event_name or '기준금리' in event_name or '연준' in event_name:
            gold_impact = "금리 동결/인하 시 달러 약세로 금 가격 강세 가능성 높음"
        elif '국채' in event_name or 'treasury' in event_name:
            gold_impact = "국채 입찰 수요 부진 시 금리 급등 및 금 가격 단기 하락 압력"
        elif '원유' in event_name or 'eia' in event_name:
            gold_impact = "원유 재고 변동에 따른 인플레이션 기대치 연동"

        report += f"*{idx}. {e['event']}*\n"
        report += f" • *날짜/시간*: {e['date']} {e['time']} (한국시간)\n"
        report += f" • *국가*: {e['country']}\n"
        report += f" • *중요도*: {e['importance']}\n"
        report += f" • *예측치*: {e['forecast']} | *이전치*: {e['previous']}\n"
        report += f" • *🥇 금 매매 영향 참고*: {gold_impact}\n"
        report += "──────────────────────\n"
        
    return report
