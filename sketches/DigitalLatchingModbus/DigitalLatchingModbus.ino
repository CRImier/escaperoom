#include <ModbusRtu.h>
#define ID   14
Modbus slave(ID, 0, 10);


const int digital_ports[] = { 2 };

#define num_digital sizeof(digital_ports)/sizeof(int)
#define reg_count 6

const bool digital_states[num_digital] = {2};
uint16_t au16data[reg_count];
uint16_t latch_register = 0;
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
  latch_register = 0;
  for(int x = 0; x < num_digital; x++)
  {
    bitWrite(latch_register, x, digitalRead(digital_ports[x]));
  }
  au16data[0] = au16data[0] | latch_register;
  au16data[reg_count-3] = slave.getInCnt();
  au16data[reg_count-2] = slave.getOutCnt();
  au16data[reg_count-1] = slave.getErrCnt();
}
