#include <ModbusRtu.h>
#define ID   3
Modbus slave(ID, 0, 10);

#define num_knobs 3

int knobs[][num_knobs] = { {A0,2},
                           {A1,3},
                           {A2,4}};

uint16_t au16data[8];


void setup() 
{
  slave.begin(115200);
}

void loop() {
  slave.poll( au16data, 8 );
  au16data[0] = 0;
  au16data[1] = 0;
  for(int x = 0; x < num_knobs; x++)
  {
    au16data[knobs[x][1]] = analogRead(knobs[x][0]);
  }
  au16data[5] = slave.getInCnt();
  au16data[6] = slave.getOutCnt();
  au16data[7] = slave.getErrCnt();
  // link the Arduino pins to the Modbus array
}
