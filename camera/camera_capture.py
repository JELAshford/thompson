# Read in pictures from the HQ camera and stream over the mqqt topics
from picamera import PiCamera
import io, os

import numpy as np

import paho.mqtt.client as mqtt
import json

def get_image(client, userdata, message):

    with PiCamera() as camera:
        camera.rotation = 180
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # return current frame
            stream.seek(0)
            _stream = stream.getvalue()
            # Convert stream to numpy format
            data = list(np.fromstring(_stream, dtype=np.uint8))
            print(data)
            # Encode and Publish to the 
            message = json.dumps(data).encode('utf-8')
            client.publish(topic="camera_feed", payload=message, qos=0, retain=False)



# Connect to the Brain client
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to request topic
client.subscribe("camera_request", qos=0)
client.message_callback_add("camera_request", get_image)

client.loop_forever()
