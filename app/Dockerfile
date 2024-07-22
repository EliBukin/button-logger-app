FROM python:3.9-alpine

ENV TZ=Asia/Jerusalem

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

RUN chmod 755 /app

ENV FLASK_APP=app:create_app() \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run"]
