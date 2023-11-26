# Plot the data from the Rpi, read through the "camera_data" topic
import paho.mqtt.client as mqtt
import pyray as pr
import json

TURN_STEP = 40
MOVE_POWER = 0.5

# Connect to the broker
broker_url, broker_port = "192.168.0.12", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)
client.loop_start()

# Window logic
pr.init_window(200, 100, "Move Interface")

command_time = pr.get_time()
command_text_lifetime = 1
command_text = None

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.draw_text("Interface! Yay!", 0, 10, 12, pr.RED)

    command = None
    if pr.is_key_down(pr.KeyboardKey.KEY_UP):
        command = [2, [1, MOVE_POWER, 0.1]]

    if pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
        command = [2, [-1, MOVE_POWER, 0.1]]

    if pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
        command = [1, [-TURN_STEP]]

    if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
        command = [1, [TURN_STEP]]

    # Send command if provided
    if command is not None:
        if pr.get_time() - command_time > 0.1:
            command_time = pr.get_time()
            command_text = str(command)
            message = json.dumps(command).encode("utf-8")
            client.publish(topic="motor_request", payload=message, qos=0, retain=False)

    # Draw command text to window, persist for 2 seconds unless overwritten
    time_since_last_command = pr.get_time() - command_time
    command_text = (
        command_text
        if time_since_last_command < command_text_lifetime
        else str(command)
    )
    pr.draw_text(f"Command: {command_text}", 0, 25, 15, pr.WHITE)
    pr.end_drawing()
pr.close_window()


# Close mqtt broker
# client.loop_stop()
