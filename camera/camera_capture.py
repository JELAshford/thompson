# Read in pictures from the HQ camera and stream over the mqqt topics
from picamera import PiCamera
import picamera.array
import io, os

import numpy as np

import paho.mqtt.client as mqtt
import json

def get_image(client, userdata, message):

    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb')
            print('Captured %dx%d image' % (
                    output.array.shape[1], output.array.shape[0]))            # Encode and Publish to the 
            message = json.dumps(output.array).encode('utf-8')
            # print(message)
            client.publish(topic="camera_feed", payload=message, qos=0, retain=False)



# Connect to the Brain client
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to request topic
client.subscribe("camera_request", qos=0)
client.message_callback_add("camera_request", get_image)

client.loop_forever()
