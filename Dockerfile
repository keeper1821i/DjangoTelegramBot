FROM ubuntu:latest
RUN apt-get update -qy
RUN apt-get install -qy python3.10 python3-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
