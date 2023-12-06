import paho.mqtt.client as mqtt
import json
import time

broker_url = ""
broker_port = 1883

client = mqtt.Client()
client.connect(broker_url, broker_port)

image = [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]
dictionary = {0: 10.3, 100: 40.5, 200: 51.2, 300: 91.2, 359: 2.0}
wheel_payload = json.dumps(image)
hq_payload = json.dumps(image[::-1])
lidar_payload = json.dumps(dictionary)

client.publish(topic="wheel_cam", payload=wheel_payload, qos=0, retain=False)
time.sleep(1)
client.publish(topic="hq_cam", payload=hq_payload, qos=0, retain=False)
time.sleep(1)
client.publish(topic="lidar", payload=lidar_payload, qos=0, retain=False)
