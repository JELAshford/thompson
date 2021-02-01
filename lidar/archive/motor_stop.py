from pyrplidar import PyRPlidar

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
# Linux   : "/dev/ttyUSB0"
# MacOS   : "/dev/cu.SLAB_USBtoUART"
# Windows : "COM5"

lidar.stop()
lidar.set_motor_pwm(0)
lidar.disconnect()
