FROM python:3.10.3

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip &&  python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=run.py

COPY . /app

