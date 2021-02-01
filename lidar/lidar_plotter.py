# Plot the data from the Rpi, read through the "lidar_data" topic
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation

import numpy as np

import paho.mqtt.client as mqtt
import json

def lidar_callback(client, userdata, message):
    global lidar_data
    decoded_message = json.loads(message.payload.decode())
    lidar_data = decoded_message
    # print(decoded_message)

def animate(i):
    global plot_angle, plot_dist, lidar_data

    if lidar_data[0] != plot_angle[-1]:
        plot_angle.append((lidar_data[0]/360)*(np.pi*2))
        plot_dist.append(lidar_data[1])

    # Re-create scatter
    ax.plot(plot_angle, plot_dist, 'r.')
    ax.set_theta_direction(-1)

# Connect to the Brain client
broker_url, broker_port = "192.168.10.103", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to lidar_data stream
client.subscribe("lidar_data", qos=0)
client.message_callback_add("lidar_data", lidar_callback)

# Storage for lidar data
lidar_data = []

# Wrap the plotting in the client loop
client.loop_start()

plot_angle, plot_dist = [0], [0]
ax = plt.subplot(111, projection='polar')
ani = FuncAnimation(plt.gcf(), animate, interval=1)
plt.show()

client.loop_stop()