
# Run on VM: docker run senrie/test-repo:producer

FROM python:3-alpine

WORKDIR /app
RUN pip3 install kafka-python

COPY . /app

ENTRYPOINT ["python3", "/app/producer.py"]
