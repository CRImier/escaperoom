// Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Reads data from an I2C/TWI slave device
// Refer to the "Wire Slave Sender" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

uint16_t uid = 0;
int counter = 0;
#include <Wire.h>

void setup()
{
  Wire.begin();        // join i2c bus (address optional for master)
  Serial.begin(115200);  // start serial for output
}

void loop()
{
  counter = 0;
  uid = 0;
  Serial.println("Sending request...");
  Wire.requestFrom(2, 2);
  while (Wire.available() && counter < 2)
  {
    Serial.println("Reading response...");
    uint16_t response = Wire.read();
    Serial.println(response, HEX);
    uid = uid | (response << counter*8);
    counter++;
  }
  Serial.print("UID is ");
  Serial.println(uid, HEX);
  delay(500);
}
