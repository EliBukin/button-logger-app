FROM alpine:3.14

WORKDIR /app

EXPOSE 5000

RUN echo "button logger app" \
&& echo "YO MON! remember to take your pills" \
&& apk add py3-pip \
&& pip install flask

ENV LC_ALL=C.UTF-8

ENV LANG=C.UTF-8

ADD ./app .

### this was added to fix the errors popping from OpenShift regarding the permissions to write to /app
RUN chgrp -R 0 /app && \
    chmod -R g=u /app

RUN apk add tzdata && \
ls /usr/share/zoneinfo && \
cp /usr/share/zoneinfo/Israel /etc/localtime && \
echo "Asia/Jerusalem" >  /etc/timezone 

RUN ["chmod", "+x", "/app/button-logger-app.py"]

ENTRYPOINT [ "python3", "/app/button-logger-app.py" ]
