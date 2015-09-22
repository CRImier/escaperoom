const int analog_ports[] = { A0, A1, A2 };
const int led_pins[] = { 6, 5, 4};

#define num_analog sizeof(analog_ports)/sizeof(int)
#define num_leds sizeof(led_pins)/sizeof(int)
#define z_treshold 600
void setup() 
{
  Serial.begin(115200);
  Serial.println("Starting AnalogReadMultiple");
  for (int x = 0; x < num_leds; x++)
  {
    pinMode(led_pins[x], OUTPUT);
  }
}

void loop() {
  for(int x = 0; x < num_analog; x++)
  {
    if (analogRead(analog_ports[x]) > z_treshold)
    {
      Serial.print("Shot detected on sensor ");
      Serial.println(x+1);
      digitalWrite(led_pins[x], HIGH);
    }
    else
    {
      digitalWrite(led_pins[x], LOW);
    }
  }
}
