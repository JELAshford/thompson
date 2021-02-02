# Plot the data from the Rpi, read through the "camera_data" topic
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation

import numpy as np

import paho.mqtt.client as mqtt
import json


def request_image(scan_parameters = "DEFAULT SCAN PLEASE"):
    global camera_data

    def camera_callback(client, userdata, message):
        global camera_data
        camera_data = json.loads(message.payload.decode())
        print(camera_data)

    # Subscribe to camera_data stream
    client.subscribe("camera_feed", qos=0)
    client.message_callback_add("camera_feed", camera_callback)

    # Publish a request to the lidar script
    message = json.dumps(scan_parameters).encode('utf-8')
    client.publish(topic="camera_request", payload=message, qos=0, retain=False)

    # Run loop to wait for data
    client.loop_start()

    # Wait for lidar data from the sensor
    camera_data = []
    while not camera_data:
        print('Waiting...', end="\r")

    client.loop_stop()

    return camera_data


def animate(i):
    # Request the scan
    camera_image = request_image()
    # Convert to usable image
    ax.imshow(camera_image)


# Connect to the broker
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Wrap the plotting in the client loop
client.loop_start()

ax = plt.subplot(111)
ani = FuncAnimation(plt.gcf(), animate, interval=1)
plt.show()

client.loop_stop()
