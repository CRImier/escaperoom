int port_mappings[][2] = {{4, 5},
                          {6, 7},
                          {8, 9}};

#define num_mappings sizeof(port_mappings)/sizeof(port_mappings[0])

void setup() {
  for(int i=0;i<num_mappings;i++)
  {
    pinMode(port_mappings[i][0], OUTPUT);
    pinMode(port_mappings[i][1], INPUT_PULLUP);
    digitalWrite(port_mappings[i][0], HIGH);
  }
  Serial.begin(115200);
}

void loop() {
  boolean conditions_met = true;
  for(int x=0;x<num_mappings;x++)
  { //Going through outputs
    digitalWrite(port_mappings[x][0], LOW); //Writing low since the inputs are pulled up
    for(int y=0;y<num_mappings;y++) //Going through the inputs
    {
      if (y == x) //If the right input is set high, that means the right wire is not connected to it
      {
        if (digitalRead(port_mappings[y][1]) == HIGH)
          conditions_met = false;
      }
      else //If wrong input is set low, that means wrong wire is connected to it
        if (digitalRead(port_mappings[y][1]) == LOW)
          conditions_met = false;
    }
    digitalWrite(port_mappings[x][0], HIGH); //Returning the previous state
  }
  Serial.println(conditions_met);
  delay(100);
}
