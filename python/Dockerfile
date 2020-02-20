FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["gunicorn", "--workers", "4", "main:app"]