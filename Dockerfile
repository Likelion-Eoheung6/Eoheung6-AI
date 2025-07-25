# Flask 컨테이너 빌드
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 필요 파일 복사
COPY app/ /app
COPY app/requirements.txt .

# 패키지 설치
RUN pip3 install --no-cache-dir -r requirements.txt

# Flask 실행
CMD ["python", "app.py"]
