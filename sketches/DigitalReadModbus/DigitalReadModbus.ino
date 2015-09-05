#include <ModbusRtu.h>
#define ID   14
Modbus slave(ID, 0, 10);


const int digital_ports[] = { 2 };

#define num_digital sizeof(digital_ports)/sizeof(int)
#define reg_count 6

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
  digitalWrite( relay_pin, bitRead( au16data[1], 0 ));
  for(int x = 0; x < num_digital; x++)
  {
    bitWrite(au16data[0], x, digitalRead(digital_ports[x]));
  }
  au16data[reg_count-3] = slave.getInCnt();
  au16data[reg_count-2] = slave.getOutCnt();
  au16data[reg_count-1] = slave.getErrCnt();
}
