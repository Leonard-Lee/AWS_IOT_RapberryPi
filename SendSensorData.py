#!/usr/bin/python
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time, json, ssl
from time import sleep

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def getNow():
    localtime = time.localtime()
    return (time.strftime("%Y%m%d_%H%M%S", localtime))

client = mqtt.Client(client_id='aws_temp_humid_client', protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='certs/root.ca.pem',
               certfile='certs/fcb5dd2aea-certificate.pem.crt',
               keyfile='certs/fcb5dd2aea-private.pem.key',
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)
client.tls_insecure_set(True)
client.connect('agwj5stucs72x.iot.us-west-2.amazonaws.com', 8883, 60)
msg = dict(id = getNow())
client.loop_start()

while True:
    sleep(2)
    if connflag == True:
        client.publish('topic', json.dumps(msg))
        print("msg sent: temperature " + "%.2f")
    else:
        print("waiting for connection...")


print getNow()
