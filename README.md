# PiBorg
Code for moving the PiBorg and reading sensor data


## Setup Notes
Uses mqtt for message passing between controller and Borg. Install mqtt broker on the Borg with: 

```bash
sudo apt install mosquitto mosquitto-clients
```

and check that it's running with: 

```bash
# Check
systemctl status mosquitto
# Stop with
service mosquitto stop 
```