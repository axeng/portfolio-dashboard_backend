FROM python:3.8

RUN pip install --upgrade pip

COPY ./requirements.txt /backend/

WORKDIR /backend

RUN pip install -r requirements.txt

COPY . /backend

ENV ENV="production"

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]