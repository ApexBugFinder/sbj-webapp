FROM python:latest AS base

ADD . /flask
WORKDIR  /flask


RUN pip3 install -r requirements.txt
RUN dir -s
EXPOSE 3700 80
WORKDIR /app/flask/sbj
CMD ["gunicorn", "wsgi:app"]
