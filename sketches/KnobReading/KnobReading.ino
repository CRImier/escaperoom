boolean error;
int num_knobs = 3;
int knobs[][3] = { {A0,174,50},
                   {A1,496,50},
                   {A2,867,50}};
  
void setup() 
{
  Serial.begin(115200);
}

void loop() {
  // read the input on analog pin 0:
  error = false;
  int x = 0;
  for(x; x < num_knobs; x++)
  {
    int knobPort = knobs[x][0];
    int minValue = knobs[x][1] - knobs[x][2];    
    int maxValue = knobs[x][1] + knobs[x][2]; 
    int reading = analogRead(knobPort);
    if (!(reading >= minValue && reading < maxValue))
       error = true;
  }
  if (error)
  {
       Serial.println("Incorrect position");
  }
  else
  {
     Serial.println("Correct position");
  }
  delay(1);
}
