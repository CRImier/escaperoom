/* Button sequence 

TODO:
Add either hardware debounce or software work-around

*/

const int buttons[]= {4, 5, 6, 7, 8, 9};
#define button_count sizeof(buttons)/sizeof(buttons[0])

const int button_sequence[]= {9, 8, 7, 6, 5, 4};
#define press_count sizeof(button_sequence)/sizeof(button_sequence[0])

bool button_states[button_count]= {};
int buttons_pressed[press_count]= {};

bool button_pressed = false;

void setup() {
  Serial.begin(115200);
  for (int x = 0; x<button_count; x++) //Setting all the button pins as inputs
  {
    pinMode(buttons[x], INPUT_PULLUP);
  }
}

void loop()
{
  for (int x = 0; x<button_count; x++) //Setting all the button pins as inputs
  {
    if (digitalRead(buttons[x]) != button_states[x]) //Comparing states to the previous states recorded
    {
      if (button_states[x] == false && digitalRead(buttons[x]) == true) //Button unpressed
      {
        button_pressed = true; //Setting a flag
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
      //Serial.print("State of button ");
      //Serial.print(buttons[x]);
      //Serial.print(" has changed to ");
      //Serial.println(button_states[x]);
      if (button_pressed == true)
      {
        for (int x = 0; x<press_count; x++) //Setting all the button pins as inputs
        {
          Serial.print(buttons_pressed[x]);
          Serial.print(" ");
        }
        Serial.println("");
      }
      button_pressed = false; //Resetting the flag
      if (memcmp(button_sequence, buttons_pressed, sizeof(button_sequence)) == 0)
      {
        Serial.println("Correct button sequence entered!");
      }
    } 
  }
}  
