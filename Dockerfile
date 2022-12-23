FROM python:latest AS base
WORKDIR  /app
ADD . /app



RUN pip3 install -r requirements.txt
RUN dir


