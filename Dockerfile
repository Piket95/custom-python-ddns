FROM python:3.11-alpine

COPY . /app
WORKDIR /app

RUN apk update && apk add --no-cache bind
RUN pip install -r requirements.txt

RUN chown root:root entrypoint.sh
RUN chmod u+x entrypoint.sh

EXPOSE 80

# CMD ["python", "main.py"]
ENTRYPOINT [ "./entrypoint.sh" ]