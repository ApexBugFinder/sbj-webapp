FROM python:latest AS base
WORKDIR  /app
ADD . /app


# EXPOSE 3700 80
RUN pip3 install -r requirements.txt
RUN ls -al
# CMD ["ls -al", ""]

