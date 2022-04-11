
# Run on VM: docker run senrie/test-repo:consumer

FROM python:3-alpine

WORKDIR /app
RUN pip3 install kafka-python

COPY . /app

ENTRYPOINT ["python3", "/app/consumer.py"]
