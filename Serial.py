import serial
import time


class Serial:
    def __init__(self, port, baud_rate):
        self.port = serial.Serial(port, baud_rate, timeout=0)
        pass

    def update(self):
        if self.port.in_waiting > 0:
            self.port.readline().decode('ascii')
        pass

    def send(self, argument):
        self.port.write(argument.encode())
