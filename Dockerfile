FROM python:3.8

RUN pip install --upgrade pip

COPY ./requirements.txt /backend/

WORKDIR /backend

RUN pip install -r requirements.txt

COPY . /backend
