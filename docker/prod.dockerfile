FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install .

CMD gunicorn hemse.app:server --bind 0.0.0.0:$8000