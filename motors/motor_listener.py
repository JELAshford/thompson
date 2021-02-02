# Read in pictures from the HQ camera and stream over the mqqt topics
import ThunderBorg
import time

import paho.mqtt.client as mqtt
import json


def PerformMove(driveLeft, driveRight, numSeconds):
    # Set the motors running
    TB.SetMotor1(driveRight * maxPower)
    TB.SetMotor2(driveLeft * maxPower)
    # Wait for the time
    time.sleep(numSeconds)
    # Turn the motors off
    TB.MotorsOff()


# Function to spin an angle in degrees
def PerformSpin(angle):
    if angle < 0.0:
        # Left turn
        driveLeft  = -1.0
        driveRight = +1.0
        angle *= -1
    else:
        # Right turn
        driveLeft  = +1.0
        driveRight = -1.0
    # Calculate the required time delay
    numSeconds = (angle / 360.0) * timeSpin360
    # Perform the motion
    PerformMove(driveLeft, driveRight, numSeconds)


# Function to drive a distance in meters
def PerformDrive(speed, time):
    print(speed, time)
    if speed < 0.0:
        # Reverse drive
        driveLeft  = -speed
        driveRight = -speed
    else:
        # Forward drive
        driveLeft  = speed
        driveRight = speed
    # Perform the motion
    PerformMove(driveLeft, driveRight, time)


def move_moters(client, userdata, message):
    command = json.loads(message.payload.decode())
    # Commmand Type: 1 = Rotate, 2 = Drive
    # Command Parameters: 
    #   1: Degrees                  [1, [90]]
    #   2: Direction, Speed, Time   [2, [1, 10, 2]]
    if command[0] == 1:
        rotation = command[1][0]
        PerformSpin(rotation)
    elif command[0] == 2:
        direction = command[1][0]
        speed = command[1][1]
        time = command[1][2]
        print(direction, speed, time)
        PerformDrive(direction * speed,  time)
    return True

# Movement settings (worked out from our MonsterBorg on carpet tiles)
timeForward1m = 0.85                    # Number of seconds needed to move about 1 meter
timeSpin360   = 1.5                    # Number of seconds needed to make a full left / right spin
testMode = False                        # True to run the motion tests, False to run the normal sequence

# Power settings
voltageIn = 12.0                        # Total battery voltage to the ThunderBorg
voltageOut = 12.0 * 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)

# Connect to the Brain client
broker_url, broker_port = "192.168.10.100", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Create ThunderBorg
TB = ThunderBorg.ThunderBorg()
TB.Init()

# Subscribe to request topic
client.subscribe("motor_request", qos=0)
client.message_callback_add("motor_request", move_moters)

client.loop_forever()
