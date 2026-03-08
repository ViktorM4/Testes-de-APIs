FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY main.py /app/

RUN useradd -m testevitor

USER testevitor

CMD ["python3", "main.py"]