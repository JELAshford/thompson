"""Liveplot the data being streamed"""
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation

import numpy as np

import socket
import json

def animate(i):
    global plot_angle, plot_dist, temp_angle, temp_dist

    # Read in and unpack the most recent data
    decoded = client.recv(1024).decode('utf-8')
    new_data = json.loads(decoded)

    temp_angle.append((new_data[0]/360)*(np.pi*2))
    temp_dist.append(new_data[1])

    # Tell server data was recieved
    client.send(json.dumps("Yep").encode('utf-8'))

    # If it's been 40 steps, add to plot data
    if i % 10 == 0:

        plot_angle += temp_angle
        plot_dist += temp_dist

        temp_angle, temp_dist = [], []

        # Re-create scatter
        ax.plot(plot_angle, plot_dist, 'r.')
        ax.set_theta_direction(-1)


# Setup client
host = '192.168.10.101'  # get local machine name
port = 8056  # Make sure it's within the > 1024 $$ <65535 range
# Connect to the server
print(host, port)
client = socket.socket()
client.connect((host, port))

# Setup plot
plot_angle, plot_dist = [], []
temp_angle, temp_dist = [], []
ax = plt.subplot(111, projection='polar')

ani = FuncAnimation(plt.gcf(), animate, interval=1)
plt.show()
