from dearpygui.core import *
from dearpygui.simple import *

from math import sin, cos, radians

import paho.mqtt.client as mqtt
import json

def lidar_callback(client, userdata, message):
    global new_data
    new_data = json.loads(message.payload.decode())

def plot_callback(sender, data):
    global new_data

    # updating plot data
    plot_datax = get_data("plot_datax")
    plot_datay = get_data("plot_datay")

    # Clear the first point from the scan if over buffer size
    if len(plot_datax) > PLOT_BUFFER_SIZE:
        plot_datax.pop(0)
        plot_datay.pop(0)

    # Add new point (convert to x/y)
    plot_datax.append(new_data[1] * cos(radians(new_data[0])))
    plot_datay.append(new_data[1] * sin(radians(new_data[0])))

    # Save plot data
    add_data("plot_datax", plot_datax)
    add_data("plot_datay", plot_datay)

    # Plot
    add_scatter_series("Plot", "Scan", plot_datax, plot_datay, weight=2)


PLOT_BUFFER_SIZE = 1000

with window("Tutorial", width=500, height=500):
    add_plot("Plot", height=-1)
    add_data("plot_datax", [])
    add_data("plot_datay", [])
    set_render_callback(plot_callback)

start_dearpygui()