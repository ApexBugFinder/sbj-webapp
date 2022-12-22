FROM python:latest AS base
WORKDIR  /app
ADD . /app
RUN pip3 install --upgrade pip
RUN python3 -m venv /app/venv
RUN source venv /opt/venv/bin/activate
RUN pip3 install -r requirements.txt
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload

