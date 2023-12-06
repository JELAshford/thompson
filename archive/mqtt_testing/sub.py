import paho.mqtt.client as mqtt
import json

broker_url = ""
broker_port = 1883


def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code " + str(rc))


def on_message(client, userdata, message):
    decoded_message = json.loads(message.payload.decode())
    print(decoded_message)


def wheel_cam_callback(client, userdata, message):
    decoded_message = json.loads(message.payload.decode())
    print("Data from Wheel Cam: ")
    print(decoded_message)


def hq_cam_callback(client, userdata, message):
    decoded_message = json.loads(message.payload.decode())
    print("Data from HQ Cam: ")
    print(decoded_message)


def lidar_callback(client, userdata, message):
    decoded_message = json.loads(message.payload.decode())
    print("Data from Lidar: ")
    print(decoded_message)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_url, broker_port)

client.subscribe("wheel_cam", qos=0)
client.subscribe("hq_cam", qos=0)
client.subscribe("lidar", qos=0)

client.message_callback_add("wheel_cam", wheel_cam_callback)
client.message_callback_add("hq_cam", hq_cam_callback)
client.message_callback_add("lidar", lidar_callback)

client.loop_forever()