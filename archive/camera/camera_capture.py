# Read in pictures from the HQ camera and stream over the mqqt topics
from picamera import PiCamera
import picamera.array
import io, os

import numpy as np
from sys import getsizeof


import paho.mqtt.client as mqtt
import json

def get_image(client, userdata, message):

    with picamera.PiCamera(resolution='640x480') as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb')
            print("Array Size: " + str(getsizeof(output.array)))
            message = json.dumps(output.array.tolist()).encode('utf-8')
            print("Message Size: " + str(getsizeof(message)))
            client.publish(topic="camera_feed", payload=message, qos=0, retain=False)


# Connect to the Brain client
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to request topic
client.subscribe("camera_request", qos=0)
client.message_callback_add("camera_request", get_image)

client.loop_forever()
