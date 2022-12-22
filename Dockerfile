FROM python:latest AS base
WORKDIR  /app
ADD . /app



RUN pip3 install -r requirements.txt
CMD ["python", "flask/sbj/wsgi.py"]

