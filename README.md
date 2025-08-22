## ✨ 이음학당 AI 서버
세대를 잇는 하루 클래스 플랫폼, **이음학당**의 AI 레포지토리입니다.

### 📌 개요
- 서비스 목표: 세대 간 소통과 재능 나눔을 위한 원데이 클래스 플랫폼 운영
- 핵심기능
    - 인기 클래스 조회
    - 간편한 UI (디지털 취약계층도 쉽게 사용할 수 있습니다.)
    - AI 맞춤 수업 추천
    - 빈집 대여하기 기능 (성북구청과 연계할 것을 전제로 기획했습니다.)

### 🛠️ 기술 스택
- Language: Python3.10
- Framework: Flask 3.1.1
- Database: MySQL, Qdrant

## 프로젝트 초기 설정
 
1. **파이썬 가상환경 생성** <br>
   최초 1회만 실행하면 됩니다.
```bash
python3 -m venv .venv
```

**각 운영체제 명령어**
| 운영체제     | 명령어                       |
|--------------|------------------------------|
| **Windows**  | `venv\Scripts\activate`      |
| **macOS/Linux** | `source venv/bin/activate` |
 
2. **의존성 다운로드**
```bash
pip3 install -r requirements.txt
```

3. **환경변수 파일** <br>
   ⚙️ .env 파일을 생성하여, Database Endpoint & API key 설정하여야 합니다.
 
