# FROM strm/dnsmasq
FROM python:3.11-alpine
# but i need python + dnsmasq or php + dnsmasq

RUN apk update && apk add bind
RUN /usr/sbin/named -c /etc/bind/named.conf

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]