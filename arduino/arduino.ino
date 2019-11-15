#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN        52 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 60 * 20 // Popular NeoPixel ring size

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 0 // Time (in milliseconds) to pause between pixels
String inputString = "";
bool stringComplete = false;


void setup() {
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin();
  Serial.begin(9600);
  inputString.reserve(200);
  pixels.clear();
}

void loop() {
  while (Serial.available()) {
    int idx = Serial.readStringUntil(',').toInt();
    int r = Serial.readStringUntil(',').toInt();
    int g = Serial.readStringUntil(',').toInt();
    int b = Serial.readStringUntil('\n').toInt();

    pixels.setPixelColor(idx, pixels.Color(r, g, b));
    pixels.show();
    
    
  }
 
}
