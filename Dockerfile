FROM python:3.7
FROM python:3.7

COPY . /app
WORKDIR /app

ENV MODE server

RUN pip install -r requirements.txt

ENTRYPOINT ["python","run.py"]
