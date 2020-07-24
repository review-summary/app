FROM python:3.7.8-slim-buster

COPY app/ /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
