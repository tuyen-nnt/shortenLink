#!/usr/bin/python3

import json
from kafka import KafkaProducer

my_producer = KafkaProducer(
    bootstrap_servers=['172.31.50.2:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html#kafka.KafkaProducer
my_producer.send('tuyen', value={'msg': 'hi'})


my_producer.flush()

# pip install -r requirement.txt
