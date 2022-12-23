FROM python:latest AS base

ADD . /app
WORKDIR  /app


RUN pip3 install -r requirements.txt
RUN dir


