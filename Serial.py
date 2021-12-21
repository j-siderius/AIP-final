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

'''
#include <WiiChuck.h>
#include <FastLED.h>

#define LED_PIN     D3
#define NUM_LEDS    12
#define BRIGHTNESS  25
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

Accessory nunchuck1;

unsigned long ledMillis, chuckMillis;

void setup() {
  Serial.begin(115200);

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(  BRIGHTNESS );

  nunchuck1.begin();
  if (nunchuck1.type == Unknown) {
    nunchuck1.type = NUNCHUCK;
  }

  ledMillis = chuckMillis = 0;
}

void loop() {
  unsigned long curMillis = millis();
  if (curMillis > ledMillis + 10) {
    ledMillis = curMillis;
    leds[0] = CRGB::Red;
    leds[1] = CRGB::Red;
    leds[2] = CRGB::Red;
    leds[3] = CRGB::Red;
    leds[4] = CRGB::Black;
    leds[5] = CRGB::Blue;
    leds[6] = CRGB::Blue;
    leds[7] = CRGB::Yellow;
    leds[8] = CRGB::Blue;
    leds[9] = CRGB::Blue;
    leds[10] = CRGB::Blue;
    leds[11] = CRGB::Black;
    FastLED.show();
  }
  if (curMillis > chuckMillis + 250) {
    chuckMillis = curMillis;
    nunchuck1.readData();    // Read inputs and update maps
    nunchuck1.printInputs(); // Print all inputs
  }
}
'''
