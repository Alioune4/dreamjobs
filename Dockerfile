FROM python:3.12.4-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# set environment variables
ENV FLASK_APP=api

# wait for the database to be ready and sync the database

EXPOSE 5000

CMD ["./entrypoint.sh"]
