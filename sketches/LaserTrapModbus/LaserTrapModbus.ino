#include <ModbusRtu.h>
#define ID   2
Modbus slave(ID, 0, 10);

int laserPin = 12;
int photoPin = A0;
int reading = 0;
int lasertocelldelay = 20; //for LDR

// the setup routine runs once when you press reset:
void setup() {
  slave.begin( 115200 );
}

uint16_t au16data[5]; // data array for modbus network sharing

int laserCheck(long mydelay)
{
  int return_code = 0;
  digitalWrite(laserPin, false);
  delay(mydelay);
  reading = analogRead(photoPin);
  if (reading > 512)
    {
      return_code = return_code | 2;
    }
  digitalWrite(laserPin, true);
  delay(mydelay);
  reading = analogRead(photoPin);
  if (reading < 512)
    {
      return_code = return_code | 1;
    }
  return return_code;
}

void modbus_io_poll() {
  au16data[1] = 0;
  int result = laserCheck(lasertocelldelay);
  if (result != 0)
  {au16data[0] = au16data[0] | result;}
  au16data[2] = slave.getInCnt();
  au16data[3] = slave.getOutCnt();
  au16data[4] = slave.getErrCnt();
}

void loop() {
  slave.poll( au16data, 5 );
  modbus_io_poll();
}
