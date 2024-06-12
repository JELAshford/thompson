# Control the ThunderBorg Board, updated for Python 3
from pathlib import Path
import fcntl
import yaml
import io


parent_dir = str(Path(__file__).resolve().parent)
with open(f"{parent_dir}/thunderborg_config.yaml") as stream:
    config = yaml.safe_load(stream)
    PARAMS, COMMANDS = config["PARAM"], config["COMMAND"]


def scan_for_thunder_borg(busNumber: int = 1):
    """Scans I²C bus (busNumber) for ThunderBorgs, returns usable addresses"""
    found = []
    print(f"Scanning I²C bus #{busNumber}")
    borg = ThunderBorg(check_chip=False)
    for address in range(0x03, 0x78, 1):
        try:
            borg.i2cAddress = address
            borg.setup_bus()
            i2cRecv = borg.RawRead(COMMANDS["GET_ID"], PARAMS["I2C_MAX_LEN"])
            if len(i2cRecv) == PARAMS["I2C_MAX_LEN"]:
                if i2cRecv[1] == PARAMS["I2C_ID_THUNDERBORG"]:
                    print(f"Found ThunderBorg at {address}")
                    found.append(address)
        except KeyboardInterrupt:
            raise
        except:
            raise
    return found


class ThunderBorg:
    def __init__(
        self, bus_number=1, i2cAddress=PARAMS["I2C_ID_THUNDERBORG"], check_chip=True
    ):
        self.foundChip = False
        self.i2cWrite = io.FileIO("/dev/null", mode="w")
        self.i2cRead = io.FileIO("/dev/null", mode="r")

        self.busNumber = bus_number
        self.i2cAddress = i2cAddress

        self.setup_bus()
        if check_chip:
            self.check_chip()

    def RawWrite(self, command, data):
        """Sends a raw command on the I2C bus to the ThunderBorg"""
        rawOutput = [command]
        rawOutput.extend(data)
        rawOutput = bytes(rawOutput)
        self.i2cWrite.write(rawOutput)

    def RawRead(self, command, length, retryCount=3):
        """Reads data back from the ThunderBorg after sending a GET command
        The function checks that the first byte read back matches the requested command
        If it does not it will retry the request until retryCount is exhausted (default is 3 times)
        """
        while retryCount > 0:
            self.RawWrite(command, [])
            rawReply = self.i2cRead.read(length)
            reply = []
            for singleByte in rawReply:
                reply.append(singleByte)
            if command == reply[0]:
                break
            else:
                retryCount -= 1
        if retryCount > 0:
            return reply
        else:
            raise IOError("I2C read for command %d failed" % (command))

    def try_read(self, command, length=PARAMS["I2C_MAX_LEN"], fail_message="Failed!"):
        try:
            i2cRecv = self.RawRead(command, length)
        except KeyboardInterrupt:
            raise
        except:
            print(fail_message)
            raise
        return i2cRecv

    def try_write(self, command, payload, fail_message):
        try:
            self.RawWrite(command, payload)
        except KeyboardInterrupt:
            raise
        except:
            print(fail_message)
            raise

    def setup_bus(self):
        self.i2cRead = io.open("/dev/i2c-" + str(self.busNumber), "rb", buffering=0)
        fcntl.ioctl(self.i2cRead, PARAMS["I2C_SLAVE"], self.i2cAddress)
        self.i2cWrite = io.open("/dev/i2c-" + str(self.busNumber), "wb", buffering=0)
        fcntl.ioctl(self.i2cWrite, PARAMS["I2C_SLAVE"], self.i2cAddress)

    def check_chip(self):
        """Check for ThunderBorg chip"""
        self.foundChip = False

        thunderborg_id = PARAMS["I2C_ID_THUNDERBORG"]
        i2cRecv = self.try_read(
            COMMANDS["GET_ID"], fail_message=f"Missing ThunderBorg at {self.i2cAddress}"
        )
        device_responded = len(i2cRecv) == PARAMS["I2C_MAX_LEN"]
        device_is_thunderborg = i2cRecv[1] == thunderborg_id

        if device_responded and device_is_thunderborg:
            self.foundChip = True
            print(
                f"Found ThunderBorg at {self.i2cAddress} loaded on bus {self.busNumber}"
            )
        elif device_responded:
            print(
                f"Found a device at {self.i2cAddress}, but it is not a ThunderBorg (ID {i2cRecv[1]} instead of {thunderborg_id})"
            )
        else:
            print(f"Missing ThunderBorg at {self.i2cAddress}")
            print(
                "Are you sure your ThunderBorg is properly attached, the correct address is used, and the I2C drivers are running?"
            )

    def get_motor_power(self, motor: int = 1):
        """Get drive level for given motor: +1 (100% fwd) to -1 (100% rev)"""
        commands = {1: COMMANDS["GET_A"], 2: COMMANDS["GET_B"]}
        i2cRecv = self.try_read(
            commands[motor], fail_message=f"Failed reading motor {motor} drive level!"
        )
        power = float(i2cRecv[2]) / float(PARAMS["PWM_MAX"])

        if i2cRecv[1] == COMMANDS["VALUE_FWD"]:
            return power
        elif i2cRecv[1] == COMMANDS["VALUE_REV"]:
            return -power
        else:
            return

    def set_motor_power(self, motor: int, power: float):
        """Set drive level for given motor: +1 (100% fwd) to -1 (100% rev)"""
        if motor == 1:
            command = COMMANDS["SET_A_REV"] if power < 0 else COMMANDS["SET_A_FWD"]
        elif motor == 2:
            command = COMMANDS["SET_B_REV"] if power < 0 else COMMANDS["SET_B_FWD"]
        else:
            raise ValueError(f"Motor '{motor}' not recognised")
        pwm = min(PARAMS["PWM_MAX"], int(abs(power) * PARAMS["PWM_MAX"]))
        self.try_write(command, [pwm], f"Failed sending motor {motor} drive level!")

    def motors_off(self):
        """Sets all motors to stopped, useful when ending a program"""
        self.try_write(COMMANDS["ALL_OFF"], [0], "Failed sending motors off command!")

    def get_led(self, led: int = 1):
        """Get RGB tuple for requested LED"""
        commands = {1: COMMANDS["GET_LED1"], 2: COMMANDS["GET_LED2"]}
        i2cRecv = self.try_read(
            commands[led], fail_message=f"Failed reading ThunderBorg LED {led} colour!"
        )
        r = i2cRecv[1] / float(PARAMS["PWM_MAX"])
        g = i2cRecv[2] / float(PARAMS["PWM_MAX"])
        b = i2cRecv[3] / float(PARAMS["PWM_MAX"])
        return r, g, b

    def set_led(self, led: int = 1, rgb=(0.0, 0.0, 0.0)):
        """Sets the current colour of the ThunderBorg LED. r, g, b may each be between 0 and 1"""
        commands = {
            0: COMMANDS["SET_LEDS"],
            1: COMMANDS["SET_LED1"],
            2: COMMANDS["SET_LED2"],
        }
        r, g, b = rgb
        levelR = max(0, min(PARAMS["PWM_MAX"], int(r * PARAMS["PWM_MAX"])))
        levelG = max(0, min(PARAMS["PWM_MAX"], int(g * PARAMS["PWM_MAX"])))
        levelB = max(0, min(PARAMS["PWM_MAX"], int(b * PARAMS["PWM_MAX"])))
        self.try_write(
            commands[led],
            [levelR, levelG, levelB],
            f"Failed sending colour for LED  {led}!",
        )

    def set_comms_failsafe(self, state: bool):
        """Enable or disable the communications failsafe, defaults to disabled at power on.
        The failsafe will turn the motors off unless it is commanded at least once every 1/4 of a second.
        """
        level = COMMANDS["VALUE_ON"] if state else COMMANDS["VALUE_OFF"]
        self.try_write(
            COMMANDS["SET_FAILSAFE"],
            [level],
            "Failed sending communications failsafe state!",
        )

    def get_comms_failsafe(self):
        """Read the current system state of the communications failsafe"""
        i2cRecv = self.try_read(
            COMMANDS["GET_FAILSAFE"],
            fail_message="Failed reading communications failsafe state!",
        )
        return i2cRecv[1] != COMMANDS["VALUE_OFF"]

    def get_drive_fault(self, motor: int = 1) -> bool:
        """Reads the motor drive fault state for given motor number.
        Faults may indicate power problems, such as under-voltage (not enough power), and may be cleared by setting a lower drive power
        For more details check the website at www.piborg.org/thunderborg and double check the wiring instructions
        """
        commands = {1: COMMANDS["GET_DRIVE_A_FAULT"], 2: COMMANDS["GET_DRIVE_B_FAULT"]}
        i2cRecv = self.try_read(
            commands[motor],
            fail_message=f"Failed reading the drive fault state for motor #{motor}!",
        )
        return i2cRecv[1] != COMMANDS["VALUE_OFF"]

    def get_battery_reading(self):
        """Reads battery level as a voltage based on the 3.3 V rail reference."""
        i2cRecv = self.try_read(
            COMMANDS["GET_BATT_VOLT"], fail_message="Failed reading battery level!"
        )
        raw = (i2cRecv[1] << 8) + i2cRecv[2]
        level = float(raw) / float(PARAMS["ANALOG_MAX"])
        level *= PARAMS["VOLTAGE_PIN_MAX"]
        return level + PARAMS["VOLTAGE_PIN_CORRECTION"]
