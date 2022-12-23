FROM python:latest AS base

ADD . /app
WORKDIR  /app


RUN pip3 install -r requirements.txt
RUN dir -s
EXPOSE 3700 80
CMD ["python3", "/flask/sbj/wsgi.py"]
