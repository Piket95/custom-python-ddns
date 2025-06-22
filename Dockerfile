FROM python:3.11-alpine

COPY . /app
WORKDIR /app

RUN apk update && apk add bind
RUN pip install -r requirements.txt

RUN chown root:root entrypoint.sh
RUN chmod u+x entrypoint.sh

# CMD ["python", "main.py"]
ENTRYPOINT [ "./entrypoint.sh" ]