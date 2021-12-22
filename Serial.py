import serial
import Screen
import math


class Serial:
    def __init__(self, port, baud_rate):
        self.port = serial.Serial(port, baud_rate, timeout=0)
        self.ledBool = True
        self.joyX, self.joyY, self.joyC, self.joyZ, self.joyC, self.joyAccX, self.joyAccY, self.joyAccZ = \
            None, None, False, False, None, None, None

    def update(self):
        waiting = self.port.in_waiting
        if waiting > 0:
            msg = self.port.read(waiting).decode('ascii')
            if 'NUNCHUCK' in msg:
                print(msg[msg.index('JoyX:'): msg.index('\r\n')])
                # calculating angle values for selection:
                # angle = math.degrees(math.atan2((JoyY-128), (JoyX-128))) + 180.0
            elif 'STATUS' in msg:
                print(msg)
            else:
                print('Serial error')

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

#include <WiiChuck.h>
#include <FastLED.h>

#define LED_PIN     D3
#define NUM_LEDS    12
#define BRIGHTNESS  25
#define LED_TYPE    WS2811
#define COLOR_ORDER RGB
CRGB leds[NUM_LEDS];

int Red = 0xFF0000;
int Green = 0x00FF00;
int Blue = 0x0000FF;
int LightBlue = 0x00000D;
int Yellow = 0xAFFF00;
int White = 0xAAAAAA;
int Black = 0x000000;

Accessory nunchuck1;

unsigned long ledMillis, controllerMillis;
int sunMoonPhase = 0; //from 0 to 11, describes the sun and moon phase >> 0=beginning of day, 5=end of daytime, 6=beginning of night, 11=end of nighttime
int healthTracker = 0; //full health=0, half health=2, dead=4
int _controllerUpdateRate = 17; //Hz=1/(millis*1000)

void setup() {
  Serial.begin(115200);

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(  BRIGHTNESS );
  FastLED.clear();

  nunchuck1.begin();
  if (nunchuck1.type == Unknown) {
    nunchuck1.type = NUNCHUCK;
  }

  ledMillis = controllerMillis = 0;
}

void loop() {
  unsigned long curMillis = millis();
  
  // LED loop
  if (curMillis > ledMillis + 1000) {
    ledMillis = curMillis;

    //health tracker
    leds[0] = Red;
    leds[1] = Red;
    leds[2] = Red;
    leds[3] = Green;
    for (int i = 4; i > -1; i--) {
      if (healthTracker - 1 >= i) leds[i] = Red;
      else leds[i] = Green;
    }

    // divider LEDs
    leds[4] = leds[11] = Black;

    // sky
    for (int j = 5; j < 11; j++) {
      if (sunMoonPhase < 6) leds[j] = Blue; //day
      else leds[j] = LightBlue; //night
    }

    // day/night cycle
    if (sunMoonPhase < 6) { //day
      leds[sunMoonPhase + 5] = Yellow;
    } else if (sunMoonPhase > 5 && sunMoonPhase < 12) { //night
      leds[sunMoonPhase - 1] = White;
    }

    if (sunMoonPhase >= 11) {
      sunMoonPhase = 0;
    } else {
      sunMoonPhase++;
    }

    FastLED.show();
  }

  // controller loop
  if (curMillis > controllerMillis + _controllerUpdateRate) {
    controllerMillis = curMillis;
    nunchuck1.readData();    // Read inputs and update maps
    nunchuck1.printInputs(); // Print all inputs
  }
}
'''
