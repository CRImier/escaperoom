#include <ModbusRtu.h>
#define ID   15
Modbus slave(ID, 0, 10);

#define num_analog 1

const int analog_ports[num_analog] = { A0 };

uint16_t au16data[2+num_analog+3];

const int relay_pin = 4;

void setup() 
{
  slave.begin(115200);
  pinMode(relay_pin, OUTPUT);
  digitalWrite(relay_pin, HIGH );
}

void loop() {
  slave.poll( au16data, 2+num_analog+3 );
  au16data[0] = 0;
  digitalWrite( relay_pin, bitRead( au16data[1], 0 ));
  for(int x = 0; x < num_analog; x++)
  {
    au16data[2+x] = analogRead(analog_ports[x]);
  }
  au16data[2+num_analog] = slave.getInCnt();
  au16data[2+num_analog+1] = slave.getOutCnt();
  au16data[2+num_analog+2] = slave.getErrCnt();
}
