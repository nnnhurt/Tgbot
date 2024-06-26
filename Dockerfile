FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
COPY fixture.json fixture.json


RUN pip install -r requirements.txt