FROM python:3.7.8-slim-buster
ENV PYTHONPATH /app:$PYTHONPATH
WORKDIR /app

COPY app/requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY app/ /app

CMD ["python", "app.py"]
