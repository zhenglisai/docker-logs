#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import json
from influxdb import InfluxDBClient
client = InfluxDBClient('192.168.58.156', 8086, '', '', 'logs')
address=('0.0.0.0',6015)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(address)
while 1:
    data,addr=s.recvfrom(2048)
    if not data:
        break
    content = json.loads(data)
    host_ip = addr[0]
    host_name = content['host']
    container_id = content['_tag']
    image_name = content['_image_name']
    container_name = content['_container_name']
    out_put = content['short_message']
    host_data = [
        {
            "measurement": "logs",
            "tags": {
                "host_name": "%s" % host_name,
                "host_ip": "%s" % host_ip,
                "container_id":"%s" %container_id,
                "image_name": "%s" %image_name,
                "container_name": "%s" %container_name
            },
            "fields": {
                "out_put": "%s" %out_put
            }
        }
    ]
    client.write_points(host_data)
s.close()