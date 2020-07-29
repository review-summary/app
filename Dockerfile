FROM python:3.7.8-slim-buster

ENV PYTHONPATH /app:$PYTHONPATH

COPY app/ /app

WORKDIR /app

RUN pip install -r /app/requirements.txt

CMD ["python", "app.py"]
