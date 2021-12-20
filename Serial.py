import serial
import Screen
import time


class Serial:
    def __init__(self, port, baud_rate):
        self.port = serial.Serial(port, baud_rate, timeout=0)
        self.ledBool = True

    def update(self):
        waiting = self.port.in_waiting
        if waiting > 0:
            msg = self.port.read(waiting).decode('ascii')
            print(msg)

        # test code
        if 18 in Screen.Screen.get_pressed_keys(self):
            print('O Pressed')
            if self.ledBool:
                self.send("on\n")
                self.ledBool = False
            else:
                self.send("off\n")
                self.ledBool = True

    def send(self, argument):
        arg = bytes(argument.encode())
        self.port.write(arg)


'''
## Arduino code: ##
String incomingBytes;
unsigned long prevMillis = 0;

void setup() {
  Serial.begin(115200);
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
  if (digitalRead(D8)) {
    Serial.write("BTN8 PRESSED");
  }
  if (millis() > prevMillis + 3000) {
    Serial.write("TIME MESSAGE");
    prevMillis = millis();
  }
}
'''
