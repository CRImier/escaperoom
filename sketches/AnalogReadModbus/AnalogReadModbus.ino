#include <ModbusRtu.h>
#define ID   11
Modbus slave(ID, 0, 10);


const int analog_ports[] = { A0, A1, A2 };

#define num_analog sizeof(analog_ports)/sizeof(int)
#define reg_count 3+num_analog+3

uint16_t au16data[reg_count];

const int relay_pin = 4;

void setup() 
{
  slave.begin(115200);
  pinMode(relay_pin, OUTPUT);
  digitalWrite(relay_pin, HIGH );
}

void loop() {
  slave.poll( au16data, reg_count );
  au16data[0] = 0;
  digitalWrite( relay_pin, bitRead( au16data[1], 0 ));
  for(int x = 0; x < num_analog; x++)
  {
    au16data[3+x] = analogRead(analog_ports[x]);
  }
  au16data[reg_count-3] = slave.getInCnt();
  au16data[reg_count-2] = slave.getOutCnt();
  au16data[reg_count-1] = slave.getErrCnt();
}
