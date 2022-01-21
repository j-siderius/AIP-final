import time
import serial
import serial.tools.list_ports

from Input import *
from Screen import *


class Serial:
    def __init__(self, port=None, baud_rate=115200, controller_moved_func=None, controller_pressed_func=None):
        """
        Initialize the serial object, specify the communication
        baud-rate and connection port. Leave port empty if you want a
        list of all available serial devices.
        :param port: serial port that the controller is connected to
        :param baud_rate: communication baud rate of the specified port
        """
        if port is None:
            self.port = None
            self.list_serial_devices()
        else:
            try:
                self.port = serial.Serial(port, baud_rate, timeout=0)
            except serial.serialutil.SerialException:
                self.port = None
                print("No Serial device connected on this address")
                self.list_serial_devices()

            self.controller_moved_func = controller_moved_func
            self.controller_pressed_func = controller_pressed_func
            self.dayNightCycle = 0
            self.health = 0
            self.joyX, self.joyY, self.joyC, self.joyZ = None, None, False, False
            self.updateDayNight(self.dayNightCycle)
            self.updateHealth(self.health)
            self.waitTime = 0

    def list_serial_devices(self):
        """
        Lists all available serial devices and their ports
        """
        print("Available serial devices:")
        serial_list = serial.tools.list_ports.comports(include_links=True)
        for element in serial_list:
            print(element.device)

    def update(self):
        """
        Serial protocol:
        send DN+00 to change day-night display
        send HLT+0 to change health display
        receive JOY:X000Y000BTZ0BTC0\r\n
        """
        if self.port is not None:
            try:
                msg = self.port.readline().decode('ascii')
                if 'JOY:' in msg:
                    self.joyX = int(msg[5:8])
                    self.joyY = int(msg[9:12])
                    self.joyZ = False if int(msg[15:16]) == 0 else True
                    self.joyC = False if int(msg[19:20]) == 0 else True

                    if self.controller_moved_func is not None and self.controller_pressed_func is not None:
                        self.controller_moved_func([self.joyX, self.joyY])
                        self.controller_pressed_func([self.joyZ, self.joyC])

                self.port.reset_input_buffer()
            except UnicodeDecodeError:
                print("decoding error")

            # test code
            if time.perf_counter() > self.waitTime + 2.000:
                self.waitTime = time.perf_counter()

                self.updateDayNight(self.dayNightCycle)  # send daynight update
                if self.dayNightCycle < 11:
                    self.dayNightCycle += 1
                else:
                    self.dayNightCycle = 0

    def updateDayNight(self, time):
        """
        Updates the time of the LED clock
        time value from 0 to 11, describes the sun and moon phase >> 0=beginning of day,
        5=end of daytime, 6=beginning of night, 11=end of nighttime
        """
        self.send('DN' + str(time).zfill(2) + "\n")

    def updateHealth(self, health):
        """
        Updates the health of the LED clock
        full health=4, half health=2, dead=0
        """
        self.send('HLT' + str(health) + "\n")

    def send(self, argument):
        if self.port is not None:
            arg = bytes(argument.encode())
            self.port.write(arg)

