# 说明该镜像以哪个镜像为基础
FROM python:3.7

COPY . /app
WORKDIR /app

ENV MODE server

# 构建者的基本信息
MAINTAINER DoubleThunder <sfyc23@gmail.com>

RUN pip install -r requirements.txt

ENTRYPOINT ["python","run.py"]
