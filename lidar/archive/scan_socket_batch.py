import numpy as np

from pyrplidar import PyRPlidar
import time

import socket
import json

BATCH_SIZE = 50

# Setup the lidar
lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
lidar.set_motor_pwm(500)
time.sleep(2)

# Print some diagnostics
info = lidar.get_info()
print("info :", info)

health = lidar.get_health()
print("health :", health)

samplerate = lidar.get_samplerate()
print("samplerate :", samplerate)


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

while True:
	# Run scan
	batch = []
	consecutive_starts = 0
	scan_generator = lidar.start_scan()
	for scan in scan_generator():
		print(scan)

		if scan.start_flag:
			consecutive_starts += 1
		if consecutive_starts > 100: break

		if scan.distance <= 3000:
			# Extract the angle and distance
			angle = scan.angle
			dist = scan.distance
			# Add to batch
			batch.append([int(angle), int(dist)])

		if len(batch) == BATCH_SIZE:
			# Package with json
			message = json.dumps(batch).encode('utf-8')
			# Send over the socket
			client_socket.send(message)

			# Wait for recipt signal
			response = json.loads(client_socket.recv(1024).decode('utf-8'))
			if response != 'GotBatch': break

			# Reset batch
			batch = []

lidar.stop()
lidar.set_motor_pwm(0)
lidar.disconnect()
