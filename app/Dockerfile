FROM python:3.9-alpine

ENV TZ=Asia/Jerusalem \
    PYTHONPATH=/app \
    FLASK_APP=app:create_app() \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_ENV=production

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /app/app-data && \
    touch /app/app-data/button_log.txt

COPY . .

RUN chmod 755 /app

EXPOSE 5000

CMD ["flask", "run"]
