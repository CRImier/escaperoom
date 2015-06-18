//COMMENT!
int laserPin = 12;
int photoPin = A0;
int reading = 0;
int delay = 14;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);

}

void calibrate()
{
  
  
}

boolean laserCheck(long mydelay)
{
  boolean noError = true;
  digitalWrite(laserPin, true);
  delay(mydelay);
  reading = analogRead(photoPin);
  if (reading < 512)
    {
      //Serial.println("Incorrect reading when laser on");
      noError = false;
    }
  digitalWrite(laserPin, false);
  delay(mydelay);
  reading = analogRead(photoPin);
  if (reading > 512)
    {
      //Serial.println("Incorrect reading when laser on");
      noError = false;
    }
  delay(mydelay);
  return noError;
}

// the loop routine runs over and over again forever:
void loop() {
    boolean error = true;
    long value = 0;
    for (mydelay = 10; mydelay <20; mydelay = mydelay + 1)
    {
      //Serial.print("Delay length:");
      //Serial.println(mydelay);
      boolean noError = laserCheck(mydelay);
      if (noError && value == 0)
      {
        error = false;
        value = mydelay;
      }  
    }
    if (!error)
      {Serial.print("First value without error:");Serial.println(value);}
}
