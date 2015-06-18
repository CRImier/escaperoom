int sensorValue;
// the setup routine runs once when you press reset:
void setup() 
{
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
}

// the loop routine runs over and over again forever:
void loop() 
{
  sensorValue = analogRead(A0);
  Serial.print(sensorValue);
  Serial.print(" ");
  delay(1);
  sensorValue = analogRead(A1);
  Serial.print(sensorValue);
  Serial.print(" ");
  delay(1);
  sensorValue = analogRead(A2);
  Serial.print(sensorValue);
  Serial.println("");
  delay(100);
}

