from dearpygui.core import *
from dearpygui.simple import *

from math import sin, cos, radians

import paho.mqtt.client as mqtt
import json


def lidar_callback(client, userdata, message):
    global new_data
    new_data = json.loads(message.payload.decode())


def plot_callback(sender, data):
    global new_data, plotted_points

    # updating plot data
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")

    # Clear the first point from the scan if over buffer size
    if len(plot_datax) > PLOT_BUFFER_SIZE:
        plot_datax.pop(0)
        plot_datay.pop(0)

    # Add new point (convert to x/y)
    if new_data:
        plot_datax.append(new_data[1] * cos(radians(new_data[0])))
        plot_datay.append(new_data[1] * sin(radians(new_data[0])))

        # Save plot data
        add_data("plot_datax", plot_datax)
        add_data("plot_datay", plot_datay)

        # Plot
        add_scatter_series("Plot", "Scan", plot_datax, plot_datay, weight=2)

        plotted_points += 1
        print(plotted_points)

PLOT_BUFFER_SIZE = 1000
new_data = []
plotted_points = 0

# Connect to the Brain client
broker_url, broker_port = "192.168.43.210", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to lidar_data stream
client.subscribe("lidar_data", qos=0)
client.message_callback_add("lidar_data", lidar_callback)


with window("Tutorial", width=500, height=500):
    add_plot("Plot", height=-1)
    add_data("plot_datax", [])
    add_data("plot_datay", [])
    set_render_callback(plot_callback)

client.loop_start()

start_dearpygui()

client.loop_stop()
