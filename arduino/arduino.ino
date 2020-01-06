#include <string.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

#define PIN        52 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 60 * 21 // Popular NeoPixel ring size

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 0 // Time (in milliseconds) to pause between pixels

void setup() {
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin();
  Serial.begin(76800);
  pixels.clear();
  pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  pixels.show();
}

void loop() {
  while (Serial.available()) {
    byte opbuf[1];
    
    Serial.readBytes(opbuf, 1);

    if (opbuf[0] == 0x00) {
      pixels.clear();
      Serial.write('E');
    } else if (opbuf[0] == 0x01) {
      byte showbuf[5];

      Serial.readBytes(showbuf, 5);

      int idx0 = showbuf[0];
      int idx1 = showbuf[1];
      int idx = idx0;
      idx = (idx << 8) | idx1;


      
      int r = showbuf[2];
      int g = showbuf[3];
      int b = showbuf[4];
    
      pixels.setPixelColor(idx, pixels.Color(r, g, b));
      Serial.write('E');
    } else if (opbuf[0] == 0x02) {
      // publish
      pixels.show();
      Serial.write('E');
    }    
  }
 
}
