# Plot the data from the Rpi, read through the "lidar_data" topic
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pylab as plt

import numpy as np

import paho.mqtt.client as mqtt
import json


def request_scan():
    global lidar_data

    def lidar_callback(client, userdata, message):
        global lidar_data
        lidar_data = json.loads(message.payload.decode())

    # Subscribe to lidar_data stream
    client.subscribe("lidar_batch", qos=0)
    client.message_callback_add("lidar_batch", lidar_callback)

    # Publish a request to the lidar script
    message = json.dumps("SCAN PLEASE").encode('utf-8')
    client.publish(topic="lidar_request", payload=message, qos=0, retain=False)

    # Run loop to wait for data
    client.loop_start()

    # Wait for lidar data from the sensor
    lidar_data = []
    while not lidar_data:
        print('Waiting...', end="\r")

    client.loop_stop()

    return lidar_data


# Connect to the broker
broker_url, broker_port = "192.168.10.103", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Create multiple plots
fig, ax = plt.subplots(2, 2, subplot_kw={'projection': 'polar'})

for x in range(2):
    for y in range(2):
        # Request the scan
        scan_data = request_scan()

        # Extract angles and dists
        scan_data = np.array(scan_data)
        plot_dists = scan_data[:, 1]
        plot_angles = (scan_data[:, 0]/360)*(np.pi*2)

        # ax = plt.subplot(111, projection='polar')
        ax[x, y].plot(plot_angles, plot_dists, 'r.')
        ax[x, y].set_theta_direction(-1)
plt.tight_layout()
plt.show()
