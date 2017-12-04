#!/usr/bin/python
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time, json, ssl
from time import sleep
import netifaces as ni
import Adafruit_DHT

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

def temphumid():
    sensor_args = {'11': Adafruit_DHT.DHT11,
                   '22': Adafruit_DHT.DHT22,
                   '2302': Adafruit_DHT.AM2302}
    sensor = sensor_args['11']
    pin = 17  ##BCM PIN PORT

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Un-comment the line below to convert the temperature to Fahrenheit.
    temperature = temperature * 9 / 5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        '{:0.2f}'.format(3.141592653589793)
        strTemp = '{:0.2f}*F'.format(temperature)
        strHumidity = '{:0.2f}%'.format(humidity)
        return (strTemp, strHumidity)
    else:
        return ('-9999.99', '-9999.99')

def getIP():
    # get the private IP
    private_ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    return private_ip

client = mqtt.Client(client_id='aws_temp_humid_client', protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='certs/root.ca.pem', keyfile='certs/fcb5dd2aea-private.pem.key', certfile='certs/fcb5dd2aea-certificate.pem.crt', tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(True)
client.connect('agwj5stucs72x.iot.us-west-2.amazonaws.com', 8883, 60)
temp, humid = temphumid()
ip = getIP()
msg = dict(temperature = temp, humidity = humid, ip = ip, timestamp = getNow())
print(msg)
client.loop_start()

while True:
    sleep(2)
    if connflag == True:
        client.publish('sensors', json.dumps(msg))
        print("msg sent: temperature " + "%.2f")
    else:
        print("waiting for connection...")
