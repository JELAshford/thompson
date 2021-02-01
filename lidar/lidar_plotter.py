# Plot the data from the Rpi, read through the "lidar_data" topic
import paho.mqtt.client as mqtt
import json

def lidar_callback(client, userdata, message):
    decoded_message = json.loads(message.payload.decode())
    print(decoded_message)

# Connect to the Brain client
broker_url, broker_port = "192.168.10.103", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to lidar_data stream
client.subscribe("lidar_data", qos=0)
client.message_callback_add("lidar_data", lidar_callback)
