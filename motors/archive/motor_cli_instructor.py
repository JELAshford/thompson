# Plot the data from the Rpi, read through the "camera_data" topic
import paho.mqtt.client as mqtt
import json

# Connect to the broker
broker_url, broker_port = "192.168.43.210", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Wrap the commands issuing in a loop
try:
    client.loop_start()
    while True:
        command = eval(input())
        # Publish a request to the motor topic
        message = json.dumps(command).encode('utf-8')
        client.publish(topic="motor_request", payload=message, qos=0, retain=False)

finally:
    client.loop_stop()
