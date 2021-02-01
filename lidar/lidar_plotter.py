# Plot the data from the Rpi, read through the "lidar_data" topic
import paho.mqtt.client as mqtt
import json

def lidar_callback(client, userdata, message):
    decoded_message = json.loads(message.payload.decode())
    print(decoded_message)

def animate(i):
    global plot_angle, plot_dist, temp_angle, temp_dist

    # Read in and unpack the most recent data
    decoded = client.recv(1024).decode('utf-8')
    new_data = json.loads(decoded)

    temp_angle.append((new_data[0]/360)*(np.pi*2))
    temp_dist.append(new_data[1])

    # Tell server data was recieved
    client.send(json.dumps("Yep").encode('utf-8'))

    # If it's been 40 steps, add to plot data
    if i % 10 == 0:

        plot_angle += temp_angle
        plot_dist += temp_dist

        temp_angle, temp_dist = [], []

        # Re-create scatter
        ax.plot(plot_angle, plot_dist, 'r.')
        ax.set_theta_direction(-1)

# Connect to the Brain client
broker_url, broker_port = "192.168.10.103", 1883
client = mqtt.Client()
client.connect(broker_url, broker_port)

# Subscribe to lidar_data stream
client.subscribe("lidar_data", qos=0)
client.message_callback_add("lidar_data", lidar_callback)

client.loop_forever()