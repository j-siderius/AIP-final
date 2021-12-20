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

'''
Arduino code:
    String incomingBytes;
    
    void setup() {
      Serial.begin(9600);
      pinMode(LED_BUILTIN, OUTPUT);
    }
    
    void loop() {
      if (Serial.available() > 0) {
        incomingBytes = Serial.readStringUntil('\n');
        if (incomingBytes == "on") {
          Serial.write("LED ON");
          digitalWrite(LED_BUILTIN, LOW);
        } else if (incomingBytes == "off") {
          Serial.write("LED OFF");
          digitalWrite(LED_BUILTIN, HIGH);
        } else {
          Serial.write("invalid");
        }
      }
    }
'''
