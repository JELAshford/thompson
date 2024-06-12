# 🎩 Thompson

Robotics test-bed with a sweet hat (it's actually a bowler hat, but there's no emoji for that)! Thompson's 'brain' is a [RaspberryPi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), with a PiBorg shield to control the wheel motors.

So far, all the code in this repository controls the ThunderBorg motors over an `mqtt` local connection. I'm gradually re-adding the sensor capabilities, and hope to have local autonomous driving in the near future.

## Basic Features

Thompson has a very simple interface written with [`raylib`](https://www.raylib.com/), which allows the user to drive Thompson around with the arrow keys.

Currently, the LIDAR and camera are not mounted but in future these will provide live feedback in the interface for the world around Thompson. I've also got an inertial measurement unit (IMU) for which I need some more wires and mounting materials, and this will allow more precise movement control.

## Setup

I use `mqtt` for message passing between the controlling computer and Thompson's Pi. Install and control the `mqtt` broker `mosquitto` on the Borg with these commands:

```bash
# Install 
sudo apt install mosquitto mosquitto-clients
# Check
systemctl status mosquitto
# Stop 
service mosquitto stop 
```

and use the `systemd` commands to locate and modify the `mosquitto` config files to allow local connections.

## Camera Notes

Info on the picamera2 module can be found [here](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) and [this script](https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server.py) works off the bat with the camera plugged in.

## Future Work

- [ ] Cleanup ThunderBorg code
- [ ] Connect IMU and report status to interface
- [ ] Connect camera and stream image back to controller
