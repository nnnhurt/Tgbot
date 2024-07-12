FROM python:3.12-alpine
ENV http_proxy http://10.8.94.101:3128 
ENV https_proxy http://10.8.94.101:3128 
WORKDIR /app

COPY requirements.txt requirements.txt
COPY fixture.json fixture.json


RUN pip install -r requirements.txt
