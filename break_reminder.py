"""
Discord Webhook 시간 알림 - 클라우드 서버용
24시간 작동 + 자동 재연결 기능 추가
"""
import os
from dotenv import load_dotenv

# .env 파일 읽기
load_dotenv() 

# 맨 처음에 시간대 설정
os.environ['TZ'] = 'Asia/Seoul'

import time
time.tzset()

import requests
import schedule
from datetime import datetime
import pytz
import sys

# ===== 설정 =====
TEST_MODE = False  # 실제 운영 시 False로 변경
WEEKEND_OFF = True  # 주말 알림 끄기 (False면 매일 작동)

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

# URL이 없으면 에러
if not WEBHOOK_URL:
    print("오류: .env 파일에 DISCORD_WEBHOOK_URL이 없습니다!")
    sys.exit(1)

KST = pytz.timezone('Asia/Seoul')

# 재시도 설정
MAX_RETRIES = 3  # 최대 재시도 횟수
RETRY_DELAY = 5  # 재시도 대기 시간 (초)


def send_webhook_message(title, description, color, fields=None):
    """
    Discord Webhook으로 메시지 전송
    
    **개념 설명**:
    - title: 알림 제목
    - description: 알림 내용
    - color: 알림 색상
    - fields: 추가 정보 (선택)
    
    **재시도 로직**: 
    실패하면 최대 3번까지 다시 시도해요
    """
    
    # 주말 체크
    # weekday(): 월요일=0, 화요일=1, ... 토요일=5, 일요일=6
    if WEEKEND_OFF:
        today = datetime.now(KST).weekday()
        if today in [5, 6]:  # 토요일(5), 일요일(6)
            print(f"주말이라 알림 건너뜀: {title}")
            return
    
    if TEST_MODE:
        # 테스트 모드: 터미널에만 출력
        print("\n" + "="*60)
        print(f" [시뮬레이션] Discord 알림")
        print("="*60)
        print(f" 제목: {title}")
        print(f" 내용: {description}")
        print(f" 색상: {hex(color)}")
        print(f" 시간: {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}")
        if fields:
            print(f" 추가 필드:")
            for field in fields:
                print(f"   • {field['name']}: {field['value']}")
        print("="*60)
        print("(테스트 모드: 실제로는 전송 안 됨)")
        return True
    else:
        # 실제 모드: Discord에 전송 (재시도 로직 추가)
        # embed: Discord의 메시지 형식
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.now(KST).isoformat(),  # ISO 형식 시간
            "footer": {"text": "시간 알림 봇"}
        }
        
        if fields:
            embed["fields"] = fields
        
        # JSON 형식으로 데이터 준비
        data = {"embeds": [embed]}
        
        # 재시도 로직
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"\n 전송 시도 {attempt}/{MAX_RETRIES}: {title}")
                
                # HTTP POST 요청으로 Discord에 전송
                response = requests.post(WEBHOOK_URL, json=data, timeout=10)
                
                # 204: 성공 (No Content - Discord가 성공 시 보내는 코드)
                if response.status_code == 204:
                    print(f" 전송 완료!")
                    return True
                else:
                    print(f"  응답 코드: {response.status_code}")
                    
                    # 마지막 시도가 아니면 재시도
                    if attempt < MAX_RETRIES:
                        print(f"⏳ {RETRY_DELAY}초 후 재시도...")
                        time.sleep(RETRY_DELAY)
                    else:
                        print(f" {MAX_RETRIES}번 시도 후 실패")
                        return False
                        
            except requests.exceptions.Timeout:
                # 타임아웃: 서버 응답이 너무 느림
                print(f" 타임아웃 발생 (10초 초과)")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    
            except requests.exceptions.ConnectionError:
                # 연결 오류: 인터넷 끊김 등
                print(f" 연결 오류 발생")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    
            except Exception as e:
                # 기타 모든 오류
                print(f" 알 수 없는 오류: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
        
        return False


# ===== 알림 함수들 =====

def test_start():
     """클라우드_테스트"""
     send_webhook_message(
         title="☀️ 테스트 알람입니다.",
         description="테스트 알람입니다",
         color=0x3498db  # 파란색
     )  



def morning_start():
    """하루 시작 10:00"""
    send_webhook_message(
        title="☀️ 하루 시작",
        description="데일리 스크럼",
        color=0x3498db  # 파란색
    )  

def morning_break():
    """오전 쉬는 시간 10:50"""
    send_webhook_message(
        title="🌤️ 쉬는 시간",
        description="쉬는 시간 입니다! 🙆‍♂️",
        color=0x3498db # 파란색
    )

def lunch_time():
    """점심 시간 11:50"""
    send_webhook_message(
        title="🍽️ 점심 시간",
        description="점심 맛있게 드세요! 😋",
        color=0xe74c3c  # 빨간색
    )

def afternoon_break():
    """오후 쉬는 시간 13:50"""
    send_webhook_message(
        title="🌤️ 쉬는 시간",
        description="쉬는 시간 입니다! 🙆‍♂️",
        color=0xf39c12  # 주황색
    )

def afternoon_break_2():
    """오후 쉬는 시간 14:50"""
    send_webhook_message(
        title="🌤️ 쉬는 시간",
        description="쉬는 시간 입니다! 🙆‍♂️",
        color=0x2ecc71  # 초록색
    )

def afternoon_break_3():
    """오후 쉬는 시간 15:50"""
    send_webhook_message(
        title="🌤️ 쉬는 시간",
        description="쉬는 시간 입니다! 🙆‍♂️",
        color=0x3498db # 파란색
    )

def afternoon_break_4():
    """오후 쉬는 시간 16:50"""
    send_webhook_message(
        title="🌤️ 쉬는 시간",
        description="쉬는 시간 입니다! 🙆‍♂️",
        color=0xf39c12 # 주황색
    )

def dinner_time():
    """저녁 시간 17:50"""
    send_webhook_message(
        title="🌙 저녁 시간",
        description="저녁 맛있게 드세요 😋",
        color=0x9b59b6  # 보라색
    )

def afternoon_break_5():
    """오후 쉬는 시간 19:50"""
    send_webhook_message(
        title="🌤️ 쉬는 시간",
        description="쉬는 시간 입니다! 🙆‍♂️",
        fields=[{
            "name": "❗데일리 과제 제출",
            "value": "데일리 과제 제출 잊지 말기!",
            "inline": True
        }],
        color=0x2ecc71 # 초록색
    )

def afternoon_break_6():
    """끝났다!!! 20:50"""
    send_webhook_message(
        title="🎉 끝났다!!!",
        description="수고하셨습니다!!!😄",
        fields=[{
            "name": "❗데일리 과제 제출",
            "value": "데일리 과제 제출 잊지 말기!",
            "inline": True
        }],
        color=0x3498db
    )    


# ===== 스케줄 설정 =====

# 실제 운영 스케줄
# schedule.every().day: 매일 실행
# .at("10:00"): 특정 시간에 실행
# .do(함수): 실행할 함수 지정

schedule.every().day.at("10:00").do(morning_start)
schedule.every().day.at("10:50").do(morning_break)
schedule.every().day.at("11:50").do(lunch_time)
schedule.every().day.at("13:50").do(afternoon_break)
schedule.every().day.at("14:50").do(afternoon_break_2)
schedule.every().day.at("15:50").do(afternoon_break_3)
schedule.every().day.at("16:50").do(afternoon_break_4)
schedule.every().day.at("17:50").do(dinner_time)
schedule.every().day.at("19:50").do(afternoon_break_5)
schedule.every().day.at("20:50").do(afternoon_break_6)


# ===== 헬스 체크 함수 (클라우드용) =====
def health_check():
    """
    봇이 살아있는지 확인하는 함수
    매 시간마다 자동 실행되어 로그를 남겨요
    """
    now = datetime.now(KST)
    print(f"\n 헬스 체크: {now.strftime('%Y-%m-%d %H:%M:%S')} - 정상 작동 중")
    
    # 다음 실행 예정 시간 출력
    next_run = schedule.next_run()
    if next_run:
        time_until = (next_run - datetime.now()).total_seconds()
        if time_until > 0:
            hours = int(time_until // 3600)
            minutes = int((time_until % 3600) // 60)
            print(f"   ⏭️  다음 알림: {next_run.strftime('%H:%M:%S')} ({hours}시간 {minutes}분 후)")

# 매 시간마다 헬스 체크 실행
schedule.every().hour.do(health_check)


# ===== 메인 실행 =====
if __name__ == '__main__':
    print("=" * 70)
    if TEST_MODE:
        print(" Discord 시간 알림 - 테스트 모드")
    else:
        print(" Discord 시간 알림 - 클라우드 실행 모드")
    print("=" * 70)
    
    # 현재 시간
    now = datetime.now(KST)
    print(f"\n 현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" 요일: {now.strftime('%A')}")
    
    # 주말 체크 상태
    if WEEKEND_OFF:
        print(" 주말 알림: OFF (평일만 작동)")
    else:
        print(" 주말 알림: ON (매일 작동)")
    
    # 모드 안내
    if TEST_MODE:
        print("\n 테스트 모드 활성화!")
        print("   → Discord에 실제로 알림이 가지 않습니다.")
        print("   → 터미널에만 출력됩니다.")
    else:
        print("\n 실제 운영 모드!")
        print("   → Discord에 실제로 알림이 전송됩니다.")
        print("   → 재시도 기능 활성화 (최대 3번)")
    
    # 등록된 스케줄
    print(f"\n 등록된 스케줄: 총 {len(schedule.jobs)}개")
    for i, job in enumerate(schedule.jobs, 1):
        print(f"  {i}. {job}")
    
    # 다음 실행 예정
    next_run = schedule.next_run()
    if next_run:
        time_until = (next_run - datetime.now()).total_seconds()
        if time_until > 0:
            hours = int(time_until // 3600)
            minutes = int((time_until % 3600) // 60)
            seconds = int(time_until % 60)
            
            print(f"\n⏭  다음 실행: {next_run.strftime('%H:%M:%S')}")
            if hours > 0:
                print(f"   ({hours}시간 {minutes}분 {seconds}초 후)")
            else:
                print(f"   ({minutes}분 {seconds}초 후)")
    
    print("\n 종료하려면 Ctrl+C를 누르세요.")
    print("="*70)
    print()
    
    # 무한 루프
    try:
        last_minute = -1
        error_count = 0  # 연속 오류 카운트
        
        while True:
            try:
                now = datetime.now(KST)
                current_time = now.strftime('%H:%M:%S')
                
                # 1분마다 한 번씩 시간 출력
                if now.minute != last_minute:
                    print(f" 대기 중... {current_time}")
                    last_minute = now.minute
                    error_count = 0  # 정상 작동 시 에러 카운트 초기화
                
                # 스케줄 실행
                schedule.run_pending()
                time.sleep(1)
                
            except KeyboardInterrupt:
                # 사용자가 Ctrl+C로 중단
                raise
                
            except Exception as e:
                # 예상치 못한 오류 발생
                error_count += 1
                print(f"\n  오류 발생 ({error_count}번째): {e}")
                
                # 10번 연속 오류 시 프로그램 종료
                if error_count >= 10:
                    print("\n 연속 오류가 너무 많습니다. 프로그램을 종료합니다.")
                    sys.exit(1)
                
                # 잠시 대기 후 계속 실행
                time.sleep(5)
                print("🔄 재시작 시도...")
            
    except KeyboardInterrupt:
        print("\n\n 프로그램을 종료합니다. 수고하셨습니다!")
        if TEST_MODE:
            print("\n 실제 운영 시: TEST_MODE = False로 변경 후 실행하세요!")
    except Exception as e:
        print(f"\n\n 치명적 오류 발생: {e}")
        print("프로그램을 종료합니다.")
        sys.exit(1)
