FROM python:3.9-slim

RUN apt-get update && apt-get install -y tzdata

ENV TZ=Asia/Jerusalem

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask python-dotenv

EXPOSE 5000

ENV FLASK_APP=app:create_app()
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

RUN chmod 755 /app

CMD ["flask", "run"]