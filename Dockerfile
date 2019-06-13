FROM python:3.6

COPY . /app
WORKDIR /app

ENV MODE server

RUN pip install -r requirements.txt

ENTRYPOINT ["python","run.py"]
