import time
import serial
import serial.tools.list_ports
from Screen import *


class Serial:
    def __init__(self, port=None, baud_rate=115200):
        """
        Initialize the serial object, specify the communication
        baud-rate and connection port. Leave port empty if you want a
        list of all available serial devices.
        """
        if port is None:
            self.port = None
            print("No serial device specified, available serial devices:")
            serial_list = serial.tools.list_ports.comports(include_links=True)
            for element in serial_list:
                print(element.device)
        else:
            try:
                self.port = serial.Serial(port, baud_rate, timeout=0)
            except serial.serialutil.SerialException:
                self.port = None
                print("No Serial device connected on this address")

            self.dayNightCycle = 0
            self.health = 0
            self.joyX, self.joyY, self.joyC, self.joyZ = None, None, False, False
            self.updateDayNight(self.dayNightCycle)
            self.updateHealth(self.health)
            self.waitTime = 0

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
                    # TODO: fix uniform circle angles!
                    # degrees on the circle:
                    #       270
                    # 0/360     180
                    #       90
                    # TODO: add check if joystick is not in the middle (then no direction should be chosen)
                    angle = int(math.degrees(math.atan2((self.joyY-128), (self.joyX-128))) + 180.0)
                    print(f"joystick{angle=}")
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


"""
## Arduino code: ##

#include <WiiChuck.h>
#include <FastLED.h>

#define LED_PIN     D3
#define NUM_LEDS    12
#define BRIGHTNESS  25
#define LED_TYPE    WS2811
#define COLOR_ORDER RGB
CRGB leds[NUM_LEDS];

int Red = 0x0A0000;
int Green = 0x000A00;
int Blue = 0x0A0AFF;
int LightBlue = 0x00000D;
int Yellow = 0xAFFF00;
int White = 0xAAAAAA;
int Black = 0x000000;

Accessory nunchuck1;

unsigned long ledMillis, controllerMillis;
String incomingBytes;
int sunMoonPhase = 0; //from 0 to 11, describes the sun and moon phase >> 0=beginning of day, 5=end of daytime, 6=beginning of night, 11=end of nighttime
int healthTracker = 4; //full health=4, half health=2, dead=0
int _controllerUpdateRate = 10; //Hz=1/(millis*1000) >> 17
uint8_t joystickX, joystickY, btnC, btnZ;

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
  if (Serial.available() > 0) {
    serialLoop();
  }

  unsigned long curMillis = millis();
  if (curMillis > ledMillis + 100) {
    ledMillis = curMillis;
    ledLoop();
  }
  if (curMillis > controllerMillis + _controllerUpdateRate) {
    controllerMillis = curMillis;
    controllerLoop();
  }
}

void serialLoop() {
  incomingBytes = Serial.readStringUntil('\n');

  //decoding
  if (incomingBytes.indexOf("DN") >= 0) {
    //daynight update
    sunMoonPhase = incomingBytes.substring(2).toInt();
  }
  if (incomingBytes.indexOf("HLT") >= 0) {
    //health update
    healthTracker = incomingBytes.substring(3).toInt();
  }
}

void ledLoop() {
  FastLED.clear();

  // divider LEDs
  leds[4] = leds[11] = Black;

  // sky
  for (int i = 5; i < 11; i++) {
    if (sunMoonPhase < 6) leds[i] = Blue; //day
    else leds[i] = LightBlue; //night
  }

  // day/night cycle
  if (sunMoonPhase < 6) { //day
    leds[sunMoonPhase + 5] = Yellow;
  } else if (sunMoonPhase > 5 && sunMoonPhase < 12) { //night
    leds[sunMoonPhase - 1] = White;
  }


  //health tracker.
  //full health=4, half health=2, dead=0
  if (healthTracker == 0) {
    leds[0] = leds[1] = leds[2] = leds[3] = Red;
  } else if (healthTracker == 1) {
    leds[0] = leds[1] = leds[2] = Red;
    leds[3] = Green;
  } else if (healthTracker == 2) {
    leds[0] = leds[1] = Red;
    leds[2] = leds[3] = Green;
  } else if (healthTracker == 3) {
    leds[0] = Red;
    leds[1] = leds[2] = leds[3] = Green;
  } else if (healthTracker >= 4) {
    leds[0] = leds[1] = leds[2] = leds[3] = Green;
  }

  FastLED.show();
}

void controllerLoop() {
  nunchuck1.readData();    // Read inputs and update maps
  joystickX = nunchuck1.values[0];  // fetch all controller inputs
  joystickY = nunchuck1.values[1];
  if (nunchuck1.values[10] > 0) btnZ = 1;
  else btnZ = 0;
  if (nunchuck1.values[11] > 0) btnC = 1;
  else btnC = 0;
  printf("JOY:X%03dY%03dBTZ%dBTC%d\r\n", joystickX, joystickY, btnZ, btnC);   // print controller inputs to serial
}
"""
