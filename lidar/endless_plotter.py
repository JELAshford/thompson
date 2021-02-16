from dearpygui.core import *
from dearpygui.simple import *

from math import sin, cos, radians

import paho.mqtt.client as mqtt
import json


def lidar_callback(client, userdata, message):
    global message_count 
    new_data = json.loads(message.payload.decode())
    message_count += 1
    print(f"Recieved: {message_count}")

    if new_data:

        print(new_data)
        print(len(new_data))
        # updating plot data
        plot_datax = get_data("plot_datax")
        plot_datay = get_data("plot_datay")

        # If there's already a full list of points, remove the first
        if len(plot_datax) > PLOT_BUFFER_SIZE:
            plot_datax.pop(0); plot_datay.pop(0)

        plot_datax.append(new_data[1] * cos(radians(new_data[0])))
        plot_datay.append(new_data[1] * sin(radians(new_data[0])))

        add_data("plot_datax", plot_datax)
        add_data("plot_datay", plot_datay)


def plot_callback(sender, data):
    # Plot current plot data
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")
    add_scatter_series("Plot", "Scan", plot_datax, plot_datay, weight=2)

PLOT_BUFFER_SIZE = 1000
plotted_points = 0
message_count = 0

# Connect to the Brain client
broker_url, broker_port = "192.168.43.210", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to lidar_data stream
client.subscribe("lidar_stream", qos=0)
client.message_callback_add("lidar_stream", lidar_callback)

with window("Tutorial", width=500, height=500):
    add_plot("Plot", height=-1)
    add_data("plot_datax", [])
    add_data("plot_datay", [])
    set_render_callback(plot_callback)

client.loop_start()

start_dearpygui()

client.loop_stop()
