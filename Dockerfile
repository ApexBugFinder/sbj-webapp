FROM python:latest AS base
WORKDIR  /app
ADD . /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload
