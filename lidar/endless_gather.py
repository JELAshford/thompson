from pyrplidar import PyRPlidar
import time

import paho.mqtt.client as mqtt
import json


# Setup the lidar
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
lidar.set_motor_pwm(500)
print('Spinning up...')
time.sleep(2)
print('...ready!')

# Connect to the Brain client
broker_url, broker_port = "192.168.1.230", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

try: 
    while True:
        # Start the lidar scan
        lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
        # Run scan
        scan_generator = lidar.force_scan()
        for count, scan in enumerate(scan_generator()):
            # print(count, scan)
            # Reset scan after a large number of scans with this generator
            # if count > 5000: break
            # Package with json and send
            message = json.dumps([scan.angle, scan.distance]).encode('utf-8')
            client.publish(topic="lidar_stream", payload=message, qos=0, retain=False)
        lidar.stop()
        lidar.disconnect()
finally:
    # Stop the lidar
    lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
    lidar.set_motor_pwm(0)
    lidar.stop()
    lidar.disconnect()