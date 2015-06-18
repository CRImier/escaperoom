int laserPin = 12;
int photoPin = A0;
int reading = 0;
int lasertocelldelay = 20;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);

}

int laserCheck(long mydelay)
{
  int return_code = 0;
  digitalWrite(laserPin, true);
  delay(mydelay);
  reading = analogRead(photoPin);
  if (reading < 512)
    {
      //Serial.println("Incorrect reading when laser on");
      return_code = return_code | 1;
    }
  digitalWrite(laserPin, false);
  delay(mydelay);
  reading = analogRead(photoPin);
  if (reading > 512)
    {
      //Serial.println("Incorrect reading when laser on");
      return_code = return_code | 2;
    }
  //delay(mydelay);
  return return_code;
}

void loop() {
  // put your main code here, to run repeatedly:
  int result = laserCheck(lasertocelldelay);
  if (result == 0)
  {
    Serial.println("All okay");
  }
  else if (result == 1)
  {
    Serial.println("Ray crossed");
    //tone(4, 262, 500);
    //delay(500);
    //noTone(4);
  }
  else if (result == 2)
  {
    Serial.println("Tamper detected");
  }
  else if (result == 3)
  {
    Serial.println("OMG WTF");
  }
}
