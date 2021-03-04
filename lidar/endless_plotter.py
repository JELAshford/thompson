from dearpygui.core import *
from dearpygui.simple import *

from math import sin, cos, radians

import paho.mqtt.client as mqtt
import json


def lidar_callback(client, userdata, message):
    new_data = json.loads(message.payload.decode())

    if new_data:
        # updating plot data
        plot_datax = get_data("plot_datax")
        plot_datay = get_data("plot_datay")

        # If there's already a full list of points, remove the first
        if len(plot_datax) > PLOT_BUFFER_SIZE:
            plot_datax.pop(0); plot_datay.pop(0)

        # Rotate plot 90 left
        new_data[0] -= 90

        plot_datax.append(new_data[1] * cos(radians(new_data[0])))
        plot_datay.append(new_data[1] * sin(radians(new_data[0])))

        add_data("plot_datax", plot_datax)
        add_data("plot_datay", plot_datay)


def plot_callback(sender, data):
    set_window_pos("Real-Time Scan Plot", x=0, y=0)
    # Plot current plot data
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")
    add_scatter_series(
        "Plot", "Scan", plot_datax, plot_datay, 
        weight=2, outline=[0, 255, 0],
        update_bounds=False
    )


def save_buffer(sender, data):
    """Save the current plot buffer data (plot_datax, plot_datay)"""
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")
    filename = get_value("Filename")
    with open(f"{BUFFER_SAVE_PATH}/{filename}.json", "w") as json_file:
        json.dump([plot_datax, plot_datay], json_file)


BUFFER_SAVE_PATH = "/Users/jamesashford/Data Store/ThompsonData/lidar_scans"
PLOT_BUFFER_SIZE = 400

# Connect to the Brain client
broker_url, broker_port = "172.20.10.11", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to lidar_data stream
client.subscribe("lidar_stream", qos=0)
client.message_callback_add("lidar_stream", lidar_callback)

with window("Real-Time Scan Plot", width=800, height=900):
    add_plot("Plot", equal_aspects=True, yaxis_invert=True, no_legend=True, height=800)
    add_data("plot_datax", [])
    add_data("plot_datay", [])
    add_separator()
    add_button("Save Buffer", callback=save_buffer)
    add_same_line()
    add_input_text("Filename", default_value="test")
    set_render_callback(plot_callback)

# Run the window and mqtt client loop
client.loop_start()
set_main_window_size(800, 900)
start_dearpygui(primary_window="Real-Time Scan Plot")
client.loop_stop()
