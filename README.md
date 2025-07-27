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
 
