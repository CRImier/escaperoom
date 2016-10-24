/*
Cat feeder indicator sketch
Hardware:
MAX7219-controlled 8-digit 7-segment display
DS1307 RTC on HW I2C bus with VBAT connected to A0 pin of Arduino - to check battery status
SPI EEPROM (forgot model) TO_ADD (no code to work with it yet, using built-in EEPROM for prototyping)
One button with one pin connected to VCC and another to D2, with pulldown to ground
TODO: add more buttons and HW debounce circuit, remake button processing code
*/ 

#include <Timer.h> //For automatic update of clock
#include <LedControl.h> //For controlling MAX7219 that drives eight 7-segment displays
#include <Time.h>  
#include <Wire.h>  //Library for low-level transfers with DS1307 RTC
#include <DS1307RTC.h>  // a basic DS1307 library that returns time as a time_t
#include <TimeAlarms.h>
#include <EEPROM.h>

boolean RTCError = false;
volatile boolean keypress = false;
char hoursNow[3];
char minutesNow[3];
char daysNow[3];
char hoursRecorded[3];
char minutesRecorded[3];
char daysRecorded[3];
char hoursSince[3];
char minutesSince[3];
char daysSince[3];

int EEPROMAddress = 0;

int batteryPin = A0; //for reading RTC battery voltage
int lLoadPin = 4; //MAX7219 LOAD pin
int lDinPin = 3; //MAX7219 CLK pin
int lClkPin = 5; //MAX7219 DIN pin

LedControl lc=LedControl(lDinPin,lClkPin,lLoadPin,1);
Timer t;

float returnBatteryVoltage() {
  int analogValue = analogRead(batteryPin);
  float voltage = analogValue * (5.0 / 1023.0);
  return analogValue;
}
  
void setup() {
  Serial.begin(9600);
  Serial.println("Starting");
  attachInterrupt(0,KeyPress,RISING);
  setupDisplay();
  setSyncProvider(RTC.get);   // the function to get the time from the RTC
  if(timeStatus()!= timeSet) 
     RTCError = true;
  else {
     timeRecord();
     timeRefresh();
     t.every(5000, timeRefresh);
     }
   //TODO:
   //Check if time in RTC is reasonable (time from EEPROM is less than time in RTC)
   //Check battery voltage and signal about incorrect voltage somehow  
   //OHSHIT... Check from months and years... 
   //All that work on time with time-oblivious libraries and hardware is killing me...
}

void setupDisplay() {
  //Default routine suggested by LedControl library, is called once at startup
  lc.shutdown(0,false);
  /* Set the brightness to a medium values */
  lc.setIntensity(0,4);
  /* and clear the display */
  lc.clearDisplay(0);
}

void KeyPress() {
  //ISR that is called when a button is pressed
  keypress = true;
}

void timeIntToChArray(int timeInt, char (*result)[3]){
  //Converts integer 
  //Positive integers less than 100 are assumed - that's correct
  String str = String(timeInt);
  //TODO: insert check for strings longer than 3 (inl. null terminator)
  if (str.length() == 1) //Padding string with zeroes
    str = "0" + str;
  str.toCharArray(*result, str.length()+1);
}

void timeRefresh(){
  //Is called every time t(Timer instance) is refreshed - to update clock 
  timeIntToChArray(minute(), &minutesNow);
  timeIntToChArray(hour(), &hoursNow);
  timeIntToChArray(day(), &daysNow);
  calculateTimeDifference();
  timeDisplay();
}

void calculateTimeDifference(){
  //This function sets hoursSince and minutesSince globals 
  int intHoursSince = 0;
  int intMinutesSince = 0;
  int intDaysSince = 0;
  //We need to calculate difference in time between A and B
  //Input:
  //days, hours and minutes of A (all in char arrays)
  //days, hours and minutes of B (all in char arrays)
  //Output:
  //difference in hours and difference in minutes (to be converted to char arrays and put into hoursSince and minutesSince)
  //hoursSince length is 3, so every value greater than 99 is replaced with 99
  int daysA = atoi(daysRecorded);
  int hoursA = atoi(hoursRecorded);
  int minutesA = atoi(minutesRecorded);
  int daysB = atoi(daysNow);
  int hoursB = atoi(hoursNow);
  int minutesB = atoi(minutesNow);
  //Here come some operations on time, seemingly careless but working in every occasion.
  intHoursSince = 24*(daysB-daysA); //could be addition but now intHoursSince is 0
  intHoursSince = intHoursSince + hoursB - hoursA;
  intMinutesSince = minutesB - minutesA;
  if (intMinutesSince < 0) //If minutes are negative, sich as when timeA is 16:59 and timeB is 17:01
     intMinutesSince += 60; intHoursSince--; 
  if (intHoursSince > 99)
     intHoursSince = 99;
  timeIntToChArray(intHoursSince, &hoursSince);
  timeIntToChArray(intMinutesSince, &minutesSince);
  Serial.print("Hours since are:");
  Serial.println(intHoursSince);
  Serial.print("Minutes since are:");
  Serial.println(intMinutesSince);
}

void timeDisplay(){
  //Outputs time on connected MAX7219-based display
  lc.clearDisplay(0);
  lc.setChar(0,7,hoursNow[0],false);
  lc.setChar(0,6,hoursNow[1],true); //decimal point is necessary between hours and minutes
  lc.setChar(0,5,minutesNow[0],false);
  lc.setChar(0,4,minutesNow[1],false);
  lc.setChar(0,3,hoursSince[0],false);
  lc.setChar(0,2,hoursSince[1],true);
  lc.setChar(0,1,minutesSince[0],false);
  lc.setChar(0,0,minutesSince[1],false);
  }

void timeRecord(){
  //Updates record of time when button was last pressed, is called every time the button is pressed =)
  timeIntToChArray(minute(), &minutesRecorded);
  timeIntToChArray(hour(), &hoursRecorded);
  timeIntToChArray(day(), &daysRecorded);
  //char valueToStore[6];
  //write to eeprom EEPROMAddress
  timeRefresh();
}

void getTimeFromEEPROM(){
  char answer[6];
  int address = EEPROMAddress;
  //read from eeprom EEPROMAddress
  for (int i = 0; i <6; i++){ //Need to read 6 bytes
    address++;
    answer[i] = EEPROM.read(address);
  Serial.print("In EEPROM we've found: ");
  Serial.println(answer);  
  }
}

/*void sendNumberToDisplay(long number) {
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
}*/

void loop() {
  // put your main code here, to run repeatedly:
  //float batteryVoltage = returnBatteryVoltage();
  //Serial.println(batteryVoltage);
  if (RTCError)
  {
   true; //Put some kind of signal routine here
  }
  else 
  {
  if (keypress) {
    detachInterrupt(0);
    //timeRefresh();
    timeRecord();
    delay(500);
    attachInterrupt(0,KeyPress,RISING);
    keypress = false;
  }
  t.update();}
}
