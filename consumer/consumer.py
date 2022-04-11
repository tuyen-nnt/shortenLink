#!/usr/bin/python3

from kafka import KafkaConsumer
import json

my_consumer = KafkaConsumer(
    'tuyen',
    bootstrap_servers=['172.31.50.2:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='tuyen-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for msg in my_consumer:
    print(msg)
