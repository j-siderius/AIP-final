import time
import serial
import serial.tools.list_ports


class Serial:
    def __init__(self, port=None, baud_rate=115200, controller_moved_func=None, controller_pressed_func=None):
        """
        Initialize the serial object, specify the communication
        baud-rate and connection port. Leave port empty if you want a
        list of all available serial devices.
        :param port: serial port that the controller is connected to
        :param baud_rate: communication baud rate of the specified port
        :param controller_moved_func: event handler for nunchuck joystick moves
        :param controller_pressed_func: event handler for nunchuck key presses
        """
        # if there is no port specified, list all available serial devices so we can select one
        if port is None:
            self.port = None
            self.list_serial_devices()
        else:
            try:
                # try to open a communication port with the
                self.port = serial.Serial(port, baud_rate, timeout=0)
            except serial.serialutil.SerialException:
                # when the assigned port does not work / cannot connect
                self.port = None
                print("No Serial device connected on this address")
                self.list_serial_devices()

            # 'function' assignment
            self.controller_moved_func = controller_moved_func
            self.controller_pressed_func = controller_pressed_func

            # general variables
            self.dayNightCycle = 0
            self.joyX, self.joyY, self.joyC, self.joyZ = None, None, False, False

            #send the initial values to the LED clock so it is reset to default
            self.updateDayNight(self.dayNightCycle)  # start at beginning of day
            self.updateHealth(4)  # start with full health

            self.msg = None

    def list_serial_devices(self):
        """
        Lists all available serial devices and their ports so user can choose one
        """
        print("Available serial devices:")
        # get all available serial ports
        serial_list = serial.tools.list_ports.comports(include_links=True)

        # print all ports
        for element in serial_list:
            print(element.device)

    def update(self):
        """
        Tries to read controller updates from the serial port using the following protocol:
        receive JOY:X000Y000BTZ0BTC0\r\n
        """
        # only check for messages if there is actually a serial port open
        if self.port is not None:
            # check if there are bytes waiting in the serial buffer
            wait = self.port.in_waiting
            if wait > 0:
                try:
                    # read all bytes in the buffer
                    buffer = self.port.read(wait)
                    msg = str(buffer)

                    # decode the message and pick the latest (most up-to-date) controller states
                    begin = msg.rfind('JOY:')
                    end = msg.rfind('BTC')+4

                    # check if the message is of the correct length (not missing arguments)
                    if end - begin == 20:
                        try:
                            # decode message to individual variables
                            msg = msg[begin: end]
                            self.joyX = int(msg[5:8])
                            self.joyY = int(msg[9:12])
                            self.joyZ = False if int(msg[15:16]) == 0 else True
                            self.joyC = False if int(msg[19:20]) == 0 else True

                            # pass the controller states to the relevant input functions
                            if self.controller_moved_func is not None and self.controller_pressed_func is not None:
                                self.controller_moved_func([self.joyX, self.joyY])
                                self.controller_pressed_func([self.joyZ, self.joyC])

                        # error handling
                        except ValueError:
                            print("serial message error")
                except IndexError:
                    print("serial error")

    def updateDayNight(self, time: int):
        """
        Updates the time of the LED clock
        send DN+00 to change day-night display
        :param time: value from 0 to 11, describes the sun and moon phase >> 0=beginning of day,
        5=end of daytime, 6=beginning of night, 11=end of nighttime
        """
        self.send('DN' + str(time).zfill(2) + "\n")

    def updateHealth(self, health: int):
        """
        Updates the health of the LED clock
        send HLT+0 to change health display
        :param health: value from 0 to 4, describes the health status of the player, full health=4, half health=2, dead=0
        """
        self.send('HLT' + str(health) + "\n")

    def send(self, argument):
        """
        Sends the serial messages to the microcontroller using the correct encoding
        :param argument: the serial message to send
        """
        # check if there is actually a usable serial port
        if self.port is not None:
            # encode the message to the correct format
            arg = bytes(argument.encode())
            self.port.write(arg)

