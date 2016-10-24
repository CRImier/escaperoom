/*
Cat feeder indicator sketch
Hardware:
MAX7219-controlled 8-digit 7-segment display
DS1307 RTC on HW I2C bus with VBAT connected to A0 pin of Arduino - to check battery status
SPI EEPROM (forgot model) TO_ADD (no code to work with it yet, using built-in EEPROM for prototyping)
One button with one pin connected to VCC and another to D2, with pulldown to ground
TODO: add more buttons and HW debounce circuit, remake button processing code
*/ 

#include <LedControl.h> //For controlling MAX7219

volatile int counter = 0;
volatile boolean counter_updated = false;

int lLoadPin = 4; //MAX7219 LOAD pin
int lDinPin = 3; //MAX7219 CLK pin
int lClkPin = 5; //MAX7219 DIN pin
//Button descriptions: {pin_num, button_code}
int buttons[][2] = { {4, 0},
                     {5, 1} };
                      
#define num_buttons sizeof(buttons)/sizeof(buttons[0])

LedControl lc=LedControl(lDinPin,lClkPin,lLoadPin,1);
  
void setup() {
  Serial.begin(9600);
  Serial.println("Counter starting");
  attachInterrupt(0, keyPress, RISING);
  setupDisplay();
}

void setupDisplay() {
  //Default routine suggested by LedControl library, is called once at startup
  lc.shutdown(0,false);
  /* Set the brightness to a medium values */
  lc.setIntensity(0,4);
  /* and clear the display */
  lc.clearDisplay(0);
}

void keyPress() {
  //ISR that is called when a button is pressed
  for (int x = 0; x < num_buttons; x++)
  {
    if (digitalRead(buttons[x][0]))
    {
      switch (buttons[x][1]){
      case 0:
        counter--;
        break;
      case 1:
        counter++;
        break;
      }
    }
    counter_updated = true;
  }
}

void sendNumberToDisplay(long number) {
  //I'll be converting int to string and then sending digits as chars one by one
  //Seems to be the easiest way to do it
  lc.clearDisplay(0);
  String str = String(number);
  char charArray[str.length()+1];
  str.toCharArray(charArray, str.length()+1);
  int offset = 8-str.length();
  for (int i=0;i<str.length();i++) {
    lc.setChar(0,7-i-offset,charArray[i],false);
  }
}

void loop() {
  if (counter_updated) {
    sendNumberToDisplay(counter);
    counter_updated = false;
  }
}
