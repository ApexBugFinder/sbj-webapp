FROM python:latest AS base

ADD . /
WORKDIR  /


RUN pip3 install -r requirements.txt
RUN dir -s


