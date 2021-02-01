import numpy as np

from pyrplidar import PyRPlidar
import time

import socket
import json

# Setup the lidar
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
lidar.set_motor_pwm(500)
time.sleep(2)

# Setup socket broadcast server
host = '192.168.10.101'
port = 8056
print(host, port)

server = socket.socket()
server.bind((host, port))

# Wait for connection
server.listen(1)
client_socket, address = server.accept()
print("Connection from: " + str(address))

# Run scan
scan_generator = lidar.force_scan()
for count, scan in enumerate(scan_generator()):
	print(count, scan)
	# Extract the angle and distance
	angle = scan.angle
	dist = scan.distance

	# Package with json
	message = json.dumps([angle, dist]).encode('utf-8')
	# Send over the socket
	client_socket.send(message)

	# Wait for recipt signal
	response = json.loads(client_socket.recv(1024).decode('utf-8'))
	if response != 'Yep': break

	# Break after 100 scans, for testing
	if count == 1000: break

lidar.stop()
lidar.set_motor_pwm(0)
lidar.disconnect()
