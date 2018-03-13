FROM python:2.7.14-alpine3.7
WORKDIR /docker-logs
RUN pip install influxdb
COPY ./logs.py ./
CMD python logs.py
