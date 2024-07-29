FROM python:3.12.4-bullseye

WORKDIR /app

COPY ./api /app/api
COPY ./migrations /app/migrations
COPY ./config.py /app
COPY ./requirements.txt /app
COPY ./run.py /app
COPY ./entrypoint.sh /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["./entrypoint.sh"]

