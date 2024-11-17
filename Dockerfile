FROM python:3.12.3-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY finance_monitoring /app