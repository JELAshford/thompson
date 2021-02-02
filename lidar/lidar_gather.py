from pyrplidar import PyRPlidar
import time

import paho.mqtt.client as mqtt
import json


def run_scan(client, userdata, message):
    request = json.loads(message.payload.decode())
    
    MAX_SAMPLES = 1000
    SLEEP_TIME = 2
    if request != "DEFAULT SCAN PLEASE":
        MAX_SAMPLES = request["MAX_SAMPLES"]
        SLEEP_TIME = request["SLEEP_TIME"]

    # Start the lidar scan
    lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
    lidar.set_motor_pwm(500)
    time.sleep(SLEEP_TIME)

    # Storage for scan data
    SAMPLE_BATCH = []

    # Run scan
    scan_generator = lidar.start_scan()
    for scan in scan_generator():

        # If scan meets quality standard, add to BATCH
        if scan.quality > 10:
            SAMPLE_BATCH.append([scan.angle, scan.distance])

        # Break if reached the maximum number of samples
        if len(SAMPLE_BATCH) > MAX_SAMPLES:
            break

    # Package with json and send
    message = json.dumps(SAMPLE_BATCH).encode('utf-8')
    client.publish(topic="lidar_batch", payload=message, qos=0, retain=False)
    
    # Stop the lidar
    lidar.set_motor_pwm(0)
    lidar.stop()


# Connect to the Brain client
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Create the lidar object to connect to
lidar = PyRPlidar()
# lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
# lidar.set_motor_pwm(500)

# Subscribe to request topic
client.subscribe("lidar_request", qos=0)
client.message_callback_add("lidar_request", run_scan)

try:
    client.loop_forever()
finally:
    # Stop the lidar
    lidar.set_motor_pwm(0)
    lidar.stop()
    lidar.disconnect()