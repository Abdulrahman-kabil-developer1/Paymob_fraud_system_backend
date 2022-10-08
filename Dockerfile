FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /back
# RUN python -m pip install --upgrade pip
COPY requirements.txt /back/
RUN pip install -r requirements.txt

COPY . /back/

 
#env variables 