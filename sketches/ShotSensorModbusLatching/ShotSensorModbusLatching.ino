#include <ModbusRtu.h>
#define ID   14
Modbus slave(ID, 0, 10);

const int sensor_ports[] = { A0, A1, A2 };
#define num_sensors sizeof(sensor_ports)/sizeof(int)
#define z_treshold 600
#define reg_count 6

uint16_t au16data[reg_count];
uint16_t latch_register = 0;

void setup() 
{
  slave.begin(115200);
}

void loop() {
  slave.poll( au16data, reg_count );
  latch_register = 0;
  for(int x = 0; x < num_sensors; x++)
  {
    if (analogRead(sensor_ports[x]) > z_treshold)
    {
      bitWrite(latch_register, x, true);
    }
  }
  au16data[0] = au16data[0] | latch_register;
  au16data[reg_count-3] = slave.getInCnt();
  au16data[reg_count-2] = slave.getOutCnt();
  au16data[reg_count-1] = slave.getErrCnt();
}
