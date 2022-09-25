FROM python:3.8-slim-buster

WORKDIR /back

COPY requirements.txt /back/
RUN pip install -r requirements.txt

COPY . /back/

 
#env variables 