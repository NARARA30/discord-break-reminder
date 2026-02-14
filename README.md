# 🔔 부트캠프 쉬는시간 디스코드 알림봇

부트캠프 일정에 맞춰 디스코드 채널로 자동 알림을 보내주는 봇입니다.

## ✨ 주요 기능

- **정시 알림**: 하루 10번의 정해진 시간에 알림 자동 전송
- **주말 휴무**: 평일에만 작동 (설정 변경 가능)
- **안정적인 재시도**: 네트워크 오류 시 최대 3번 재시도
- **24시간 작동**: PythonAnywhere에서 무중단 실행
- **테스트 모드**: 실제 전송 없이 터미널에서 테스트 가능

## 📅 알림 시간표

| 시간 | 종류 | 설명 |
|------|------|------|
| 10:00 | ☀️ 하루 시작 | 데일리 스크럼 |
| 10:50 | 🌤️ 쉬는 시간 | 오전 휴식 |
| 11:50 | 🍽️ 점심 시간 | 점심 식사 |
| 13:50 | 🌤️ 쉬는 시간 | 오후 휴식 1 |
| 14:50 | 🌤️ 쉬는 시간 | 오후 휴식 2 |
| 15:50 | 🌤️ 쉬는 시간 | 오후 휴식 3 |
| 16:50 | 🌤️ 쉬는 시간 | 오후 휴식 4 |
| 17:50 | 🌙 저녁 시간 | 저녁 식사 |
| 19:50 | 🌤️ 쉬는 시간 | 오후 휴식 5 + 과제 알림 |
| 20:50 | 🎉 끝! | 하루 종료 + 과제 알림 |

## 🛠️ 사용 기술

- **Python 3.x**
- **Discord Webhook API** - 메시지 전송
- **requests** - HTTP 통신
- **schedule** - 시간 예약 실행
- **python-dotenv** - 환경변수 관리
- **pytz** - 시간대(한국 시간) 처리
- **PythonAnywhere** - 무료 클라우드 호스팅

## 📋 설치 및 실행 방법

### 1️⃣ 레포지토리 클론

```bash
git clone [여러분의-깃랩-레포-URL]
cd discord-break-reminder
```

### 2️⃣ 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

**requirements.txt 설명**:
```
requests - HTTP 요청을 보내는 라이브러리
python-dotenv - .env 파일에서 환경변수 읽기
schedule - 특정 시간에 함수 자동 실행
pytz - 시간대(타임존) 처리
```

### 3️⃣ 환경변수 설정

**Step 1**: `.env` 파일 생성
```bash
cp .env.example .env
```

**Step 2**: 디스코드 웹훅 URL 생성
1. 알림을 받을 디스코드 채널 선택
2. 채널 설정(⚙️) → 연동 → 웹훅
3. '새 웹훅' 버튼 클릭
4. 웹훅 이름 설정 (예: 쉬는시간 알림봇)
5. '웹훅 URL 복사' 클릭

**Step 3**: `.env` 파일 수정
```
DISCORD_WEBHOOK_URL=여기에_복사한_웹훅_URL_붙여넣기
```

### 4️⃣ 로컬에서 테스트

**테스트 모드로 실행** (Discord에 실제로 전송 안 됨):
```python
# break_reminder.py 파일 열기
TEST_MODE = True  # 이 값이 True인지 확인
```

```bash
python break_reminder.py
```

터미널에 알림 시뮬레이션이 출력되면 성공!

**실제 모드로 실행** (Discord에 진짜 전송):
```python
# break_reminder.py 파일 열기
TEST_MODE = False  # False로 변경
```

```bash
python break_reminder.py
```

디스코드 채널에 메시지가 나타나면 성공!

## 🚀 PythonAnywhere 배포 (24시간 실행)

### 1단계: PythonAnywhere 가입
- [www.pythonanywhere.com](https://www.pythonanywhere.com) 접속
- 무료 계정 생성 (Beginner account)

### 2단계: 파일 업로드
1. **Files** 탭 클릭
2. 새 디렉토리 생성: `discord-bot`
3. 다음 파일들 업로드:
   - `break_reminder.py`
   - `requirements.txt`
   - `.env` (웹훅 URL이 들어있는 파일)

### 3단계: 패키지 설치
1. **Consoles** 탭 → **Bash** 클릭
2. 다음 명령어 실행:

```bash
cd discord-bot
pip3 install -r requirements.txt --user
```

### 4단계: Screen 세션으로 봇 실행 (백그라운드 실행)

PythonAnywhere 무료 계정은 콘솔을 닫으면 프로그램이 종료돼요. 
`screen` 명령어를 사용하면 콘솔을 닫아도 프로그램이 계속 실행됩니다!

**개념 설명**:
- `screen`: 가상의 터미널 세션을 만들어주는 도구
- 콘솔을 닫아도 세션은 백그라운드에서 계속 실행돼요
- 언제든 다시 접속해서 상태를 확인할 수 있어요

#### Step 1: Screen 세션 생성

```bash
screen -S discord-bot
```

**명령어 설명**:
- `screen`: screen 프로그램 실행
- `-S`: 세션 이름 지정 (Session의 S)
- `discord-bot`: 원하는 세션 이름 (나중에 찾기 쉽게)

#### Step 2: 봇 실행

```bash
cd discord-bot
python3 break_reminder.py
```

봇이 실행되면 "대기 중..." 메시지가 1분마다 나타나요!

#### Step 3: 백그라운드로 전환

**키보드 단축키**: `Ctrl + A`, 그 다음 `D`

**개념 설명**:
- `Ctrl + A`: Screen의 명령 모드 진입
- `D`: Detach (분리) - 세션을 백그라운드로 보냄
- 화면에 `[detached from 세션번호.discord-bot]` 메시지가 나타나면 성공!

이제 콘솔을 닫아도 봇은 계속 실행됩니다! 🎉

#### Step 4: 실행 중인 세션 확인

```bash
screen -ls
```

**명령어 설명**:
- `-ls`: List Sessions (세션 목록 보기)

**출력 예시**:
```
There is a screen on:
    12345.discord-bot    (Detached)
1 Socket in /var/run/screen/S-사용자명.
```

**상태 의미**:
- `Detached`: 백그라운드에서 실행 중 (정상!)
- `Attached`: 현재 접속 중

#### Step 5: 세션 다시 접속하기 (상태 확인)

```bash
screen -r discord-bot
```

**명령어 설명**:
- `-r`: Reattach (다시 붙이기)
- `discord-bot`: 접속할 세션 이름

봇이 잘 돌아가는지 로그를 확인할 수 있어요!

다시 나가려면: `Ctrl + A`, 그 다음 `D`

#### Step 6: 봇 종료하기

세션에 접속한 상태에서:
```
Ctrl + C  (봇 종료)
exit      (세션 종료)
```

또는 세션 강제 종료:
```bash
screen -X -S discord-bot quit
```

### 5단계: 작동 확인
- `screen -ls`로 세션이 실행 중인지 확인
- `screen -r discord-bot`으로 접속해서 로그 확인
- 콘솔에 "대기 중..." 메시지가 1분마다 나타나면 정상!
- 헬스 체크가 1시간마다 자동 실행됨

### 💡 Screen 명령어 치트시트

| 명령어 | 설명 |
|--------|------|
| `screen -S 이름` | 새 세션 생성 |
| `Ctrl+A, D` | 백그라운드로 전환 |
| `screen -ls` | 실행 중인 세션 목록 |
| `screen -r 이름` | 세션에 다시 접속 |
| `screen -X -S 이름 quit` | 세션 강제 종료 |
| `exit` | (세션 안에서) 세션 종료 |

## ⚙️ 설정 변경

### 주말에도 알림 받고 싶다면?
```python
# break_reminder.py 파일 상단
WEEKEND_OFF = False  # True → False로 변경
```

### 알림 시간 변경하려면?
```python
# 스케줄 설정 부분 수정
schedule.every().day.at("10:00").do(morning_start)  # 10:00 → 원하는 시간
```

### 알림 추가/삭제
```python
# 새 알림 함수 만들기
def my_custom_alert():
    send_webhook_message(
        title="🎯 내 알림",
        description="원하는 내용",
        color=0x3498db  # 색상 코드 (16진수)
    )

# 스케줄에 추가
schedule.every().day.at("15:30").do(my_custom_alert)
```

## 🎨 색상 코드표

```python
0x3498db  # 파란색
0xe74c3c  # 빨간색
0xf39c12  # 주황색
0x2ecc71  # 초록색
0x9b59b6  # 보라색
```

## 🔧 주요 개념 설명

### Webhook이란?
- 외부 프로그램이 디스코드에 메시지를 보낼 수 있는 URL
- 봇처럼 복잡한 설정 없이 간단하게 사용 가능
- 일방향 통신 (보내기만 가능, 받기는 불가)

### Schedule 라이브러리
- 특정 시간에 함수를 자동으로 실행해주는 도구
- `schedule.every().day.at("10:00").do(함수)` 형식으로 사용
- 무한 루프 안에서 `schedule.run_pending()`으로 계속 체크

### 환경변수 (.env)
- 비밀번호나 API 키 같은 민감한 정보를 코드와 분리해서 저장
- `.env` 파일은 깃에 올리지 않음 (`.gitignore`에 포함)
- `python-dotenv`로 쉽게 불러올 수 있음

### 재시도 로직
- 네트워크 오류나 서버 문제로 실패하면 자동으로 다시 시도
- 최대 3번까지 재시도, 5초 대기 후 재시도
- 안정성 향상!

### 헬스 체크
- 1시간마다 "봇이 살아있는지" 확인
- 로그를 남겨서 문제 발생 시 디버깅 가능

## ⚠️ 주의사항

### 보안
- **웹훅 URL은 절대 공개하지 마세요!**
- 유출되면 누구나 여러분의 채널에 메시지를 보낼 수 있어요
- `.env` 파일은 깃에 커밋하지 마세요 (`.gitignore`에 포함됨)

### PythonAnywhere 무료 계정 제한
- **콘솔 자동 종료**: 직접 실행하면 콘솔 닫을 때 봇도 종료돼요 → `screen` 사용으로 해결!
- 외부 사이트 접속 제한 (discord.com은 허용됨)
- CPU 시간 제한 (하루에 100초)

### Screen 사용 시 주의사항
- PythonAnywhere 무료 계정은 3개월마다 콘솔을 한 번씩 열어줘야 해요
- 너무 오래 방치하면 계정이 비활성화될 수 있어요
- 주기적으로 `screen -r discord-bot`으로 접속해서 상태 확인을 추천해요

### 한국 시간 (KST)
- PythonAnywhere 서버는 UTC 시간대
- 코드에서 `pytz`로 자동으로 한국 시간(+9시간)으로 변환
- `os.environ['TZ'] = 'Asia/Seoul'`로 시간대 설정

## 🐛 문제 해결

### "❌ 오류: .env 파일에 DISCORD_WEBHOOK_URL이 없습니다!"
→ `.env` 파일을 만들고 웹훅 URL을 추가하세요

### "⚠️ 응답 코드: 401"
→ 웹훅 URL이 잘못되었어요. 다시 복사해서 붙여넣으세요

### "🔌 연결 오류 발생"
→ 인터넷 연결을 확인하세요

### 알림이 안 와요
→ `TEST_MODE = False`인지 확인하세요
→ 주말이면 `WEEKEND_OFF = True`인지 확인하세요

### Screen 관련 문제

**"There is no screen to be resumed"**
→ 실행 중인 screen 세션이 없어요. `screen -ls`로 확인 후 `screen -S discord-bot`으로 새로 만드세요

**Screen 세션이 여러 개 생겼어요**
```bash
# 모든 세션 확인
screen -ls

# 필요 없는 세션 종료
screen -X -S 세션이름 quit
```

**Screen에서 나가는 방법을 잊었어요**
→ `Ctrl + A`를 누른 다음 `D`를 누르세요 (Detach)

**봇이 죽었는지 확인하고 싶어요**
```bash
# 세션 목록 확인
screen -ls

# 세션에 접속해서 로그 확인
screen -r discord-bot
```

궁금한 점 있으면 언제든 물어보세요! 😊