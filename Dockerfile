# Base 이미지 설정
FROM python:3.9

ENV PYTHONUNBUFFERED 1
# 작업 디렉토리 생성 및 설정
WORKDIR /app

ENV APP_HOME=/app

# 필요한 패키지 복사
COPY requirements.txt ./

# 패키지 설치
RUN apt-get update && apt-get install -y bash && apt-get install -y build-essential\
    && apt-get install -y libgl1-mesa-glx vim\
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

EXPOSE 8000

# app user 생성 및 모든 파일 권한변경
RUN useradd -m app && chown -R app:app $APP_HOME

USER app

# RUN ["sleep", "infinity"]

# # Django 초기화 및 마이그레이션
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# Django 서버 실행
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# kafka consumer.py 실행
# CMD [ "bash", "-c", "nohup python consumer.py &" ]
# bash -c "nohup python consumer.py