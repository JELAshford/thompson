# Read in pictures from the HQ camera and stream over the mqqt topics
import thunder_borg as ThunderBorg
import paho.mqtt.client as mqtt
import json
import time


def run_motors(drive_left: int, drive_right: int, run_time: float, max_power: float = 0.8):
    TB.set_motor_power(1, drive_right * max_power)
    TB.set_motor_power(2, drive_left * max_power)
    time.sleep(run_time)
    TB.motors_off()


def move(direction: int, speed: float, time: float):
    motor_speed = direction * speed
    run_motors(motor_speed, motor_speed, time)


def spin(angle: float):
    rotate_time = abs(angle) / 360.0
    motor_directions = (-1, 1) if angle < 0 else (1, -1)
    run_motors(*motor_directions, rotate_time, max_power=0.5)


def process_motor_command(client, userdata, message):
    """Read command from controller, and dispatch to function"""
    command_store = {"move": move, "spin": spin}
    command_name, parameters = json.loads(message.payload.decode())
    command_store[command_name](**parameters)


# Connect to the Brain client
broker_url, broker_port = "192.168.0.12", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Create ThunderBorg
TB = ThunderBorg.ThunderBorg()

# Subscribe to request topic
client.subscribe("motor_request", qos=0)
client.message_callback_add("motor_request", process_motor_command)
client.loop_forever()

# Copyable kill command
# from motors import ThunderBorg; tb = ThunderBorg.ThunderBorg(); tb.Init(); tb.SetMotor1(0); tb.SetMotor2(0)