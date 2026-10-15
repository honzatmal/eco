from collector import fetch_economic_calendar
from notifier import format_report, send_telegram_message

def main():
    print("경제지표 데이터 수집 시작...")
    events = fetch_economic_calendar()
    print(f"수집된 이벤트 수: {len(events)}개")
    
    report = format_report(events)
    print("텔레그램 리포트 전송 중...")
    send_telegram_message(report)

if __name__ == '__main__':
    main()
