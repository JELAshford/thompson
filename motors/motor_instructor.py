# Plot the data from the Rpi, read through the "camera_data" topic
import paho.mqtt.client as mqtt
import json

from dearpygui.core import *
from dearpygui.simple import *


def main_callback(sender, data):
    command = None

    if is_key_pressed(mvKey_Up):
        command = [2, [1, MOVE_POWER, 0.2]]
        set_value("FORWAD key Pressed", "True")
    else:
        set_value("FORWAD key Pressed", "False")

    if is_key_pressed(mvKey_Down):
        command = [2, [-1, MOVE_POWER, 0.2]]
        set_value("BACKWARD key Pressed", "True")
    else:
        set_value("BACKWARD key Pressed", "False")

    if is_key_pressed(mvKey_Left):
        command = [1, [-TURN_STEP]]
        set_value("LEFT key Pressed", "True")
    else:
        set_value("LEFT key Pressed", "False")

    if is_key_pressed(mvKey_Right):
        command = [1, [TURN_STEP]]
        set_value("RIGHT key Pressed", "True")
    else:
        set_value("RIGHT key Pressed", "False")

    # Send command if one requested
    if command:
        print(command)
        message = json.dumps(command).encode('utf-8')
        client.publish(topic="motor_request", payload=message, qos=0, retain=False)


TURN_STEP = 20
MOVE_POWER = 0.5

# Connect to the broker
broker_url, broker_port = "192.168.43.210", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# is_key_down(mvKey_A)
with window("Move Interface"):
    add_text("Key Polling")
    add_label_text("LEFT key Pressed", default_value="False", color=[0, 200, 255])
    add_spacing()
    add_label_text("RIGHT key Pressed", default_value="False", color=[0, 200, 255])
    add_spacing()    
    add_label_text("FORWAD key Pressed", default_value="False", color=[0, 200, 255])
    add_spacing()
    add_label_text("BACKWARD key Pressed", default_value="False", color=[0, 200, 255])

set_render_callback(main_callback)

client.loop_start()
start_dearpygui(primary_window="Move Interface")
client.loop_stop()

