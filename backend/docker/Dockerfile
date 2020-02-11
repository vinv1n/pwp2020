FROM alpine:3.11

RUN apk add --no-cache python3

ADD backend/api/ /app/api/
ADD backend/__init__.py /app/
ADD backend/wsgi.py /app/

RUN pip3 install gunicorn

ADD backend/requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app/

EXPOSE 5000
