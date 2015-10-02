/* Button sequence 

Hardware debounce presence is assumed

*/
#include <ModbusRtu.h>
#define ID   10
Modbus slave(ID, 0, 10);

const int buttons[]= {4, 5, 6, 7, 8, 9};
#define button_count sizeof(buttons)/sizeof(buttons[0])
const int button_sequence[]= {9, 8, 7, 6, 5, 4};
#define press_count sizeof(button_sequence)/sizeof(button_sequence[0])
//Modbus storage
#define reg_count 3+press_count+3
uint16_t au16data[reg_count];
//Storage arrays
bool button_states[button_count]= {};
int buttons_pressed[press_count]= {};
//Some pins to be defined
const int relay_pin = 12;

void setup() {
  slave.begin(115200);
  for (int x = 0; x<button_count; x++) //Setting all the button pins as inputs
  {
    pinMode(buttons[x], INPUT_PULLUP);
  }
  pinMode(relay_pin, OUTPUT);
  digitalWrite(relay_pin, HIGH );
}

void loop()
{
  slave.poll( au16data, reg_count );
  for (int x = 0; x<button_count; x++) //Setting all the button pins as inputs
  {
    if (digitalRead(buttons[x]) != button_states[x]) //Comparing states to the previous states recorded
    {
      if (button_states[x] == false && digitalRead(buttons[x]) == true) //Button unpressed
      {
        for (int y = 0; y<button_count; y++) //Shifting the array by one
        {
          if (y == button_count-1) //Last element of array reached, putting last button number there
          {
            buttons_pressed[y] = buttons[x];
          }
          else
          {
            buttons_pressed[y] = buttons_pressed[y+1];
          }
        }
      }
      button_states[x] = digitalRead(buttons[x]);
    } 
  }
  au16data[0] = 0;
  digitalWrite( relay_pin, bitRead( au16data[1], 0 ));
  for(int x = 0; x < press_count; x++)
  {
    au16data[3+x] = buttons_pressed[x];
  }
  au16data[reg_count-3] = slave.getInCnt();
  au16data[reg_count-2] = slave.getOutCnt();
  au16data[reg_count-1] = slave.getErrCnt();
}  
