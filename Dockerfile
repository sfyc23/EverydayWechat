# 说明该镜像以哪个镜像为基础
FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
COPY . /app

ENV MODE server

# 构建者的基本信息
MAINTAINER DoubleThunder <sfyc23@gmail.com>


ENTRYPOINT ["python", "run.py"]
