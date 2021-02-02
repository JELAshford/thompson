# Plot the data from the Rpi, read through the "lidar_data" topic
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation

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


def repeat_grid(ncol=2, nrow=2):
    """Create grid of multiple plots"""
    _, ax = plt.subplots(ncol, nrow, subplot_kw={'projection': 'polar'})
    for x in range(nrow):
        for y in range(ncol):
            # Request the scan
            scan_data = request_scan()
            # Extract angles and dists
            scan_data = np.array(scan_data)
            plot_dists = scan_data[:, 1]
            plot_angles = (scan_data[:, 0]/360)*(np.pi*2)
            # Add to correct axis
            ax[y, x].plot(plot_angles, plot_dists, 'r.')
            ax[y, x].set_theta_direction(-1)
    # Show plot
    plt.tight_layout()
    plt.show()


def repeat_delay():

    def animate(i):
        # Request the scan
        scan_data = request_scan()
        # Extract angles and dists
        scan_data = np.array(scan_data)
        plot_dists = scan_data[:, 1]    
        plot_angles = (scan_data[:, 0]/360)*(np.pi*2)
        # Re-create scatter
        ax.clear()
        ax.plot(plot_angles, plot_dists, 'r.')
    
    # Wrap the plotting in the client loop
    client.loop_start()

    ax = plt.subplot(111, projection='polar')
    ax.set_theta_direction(-1)
    ani = FuncAnimation(plt.gcf(), animate, interval=1)
    plt.show()

    client.loop_stop()


# Connect to the broker
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# repeat_grid()
repeat_delay()
