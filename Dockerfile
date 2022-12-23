FROM python:latest AS base

ADD . /
WORKDIR  /flask/sbj


RUN pip3 install -r requirements.txt
RUN dir -s

CMD ["python3", "/flask/sbj/wsgi.py"]
