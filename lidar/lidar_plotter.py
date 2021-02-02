# Plot the data from the Rpi, read through the "lidar_data" topic
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pylab as plt

import numpy as np

import paho.mqtt.client as mqtt
import json


def lidar_callback(client, userdata, message):
    global lidar_data
    lidar_data = json.loads(message.payload.decode())


def request_scan():
    # Subscribe to lidar_data stream
    client.subscribe("lidar_batch", qos=0)
    client.message_callback_add("lidar_batch", lidar_callback)

    # Wrap the plotting in the client loop
    client.loop_start()

    # Publish a request to the lidar script
    message = json.dumps("SCAN PLEASE").encode('utf-8')
    client.publish(topic="lidar_request", payload=message, qos=0, retain=False)

    # Wait for lidar data from the sensor
    lidar_data = []
    while not lidar_data:
        print('Waiting...', end="\r")

    return lidar_data


# Connect to the broker
broker_url, broker_port = "192.168.10.103", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Request the scan
scan_data = request_scan()

# Extract angles and dists
scan_data = np.array(scan_data)
plot_dists = scan_data[:, 1]
plot_angles = (scan_data[:, 0]/360)*(np.pi*2)

ax = plt.subplot(111, projection='polar')
ax.plot(plot_angles, plot_dists, 'r.')
ax.set_theta_direction(-1)
plt.show()

client.loop_stop()