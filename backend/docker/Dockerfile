FROM alpine:3.11

RUN apk update && apk add --virtual build-deps postgresql-dev \
libpq gcc python3-dev musl-dev netcat-openbsd bash \
postgresql-client

ADD backend/api/ /app/api/
ADD backend/__init__.py /app/
ADD backend/wsgi.py /app/
ADD backend/scripts/weathertalk /usr/bin/weathertalk

ADD backend/tests/ /app/

RUN pip3 install gunicorn

ADD backend/requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app/

EXPOSE 5000

ENTRYPOINT [ "/usr/bin/weathertalk" ]
