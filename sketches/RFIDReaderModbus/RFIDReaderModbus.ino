#include <SPI.h>
#include <MFRC522.h>
#include <ModbusRtu.h>
#define ID   3
Modbus slave(ID, 0, 10);

#define num_readers 3


MFRC522 *readers[num_readers];

//Array with configs for each reader. 
//Structure: {RST_PIN, SS_PIN, MODBUS_REG }
int reader_settings[num_readers][3] = {{9, 10, 3},
                                       {2, 3, 4},
                                       {4, 5, 5}};

//Modbus register array.
uint16_t au16data[9] = 
{0, //Left untouched
0, //Left untouched
0, //Reader diagnostics
0, //First reader
0, //Second reader
0, //Third reader
0, //Diagnostics - packets sent
0, //Diagnostics - packets received
0};//Diagnostics - error count


void setup() {		// Initialize serial communications with the PC
  SPI.begin();			// Init SPI bus
	setup_readers();
  slave.begin(115200);
}

void setup_readers()
{ 
  for(int x = 0; x < num_readers; x++)
  {                            //{RST_PIN, SS_PIN, MODBUS_REG }
    //Creating a reader instance
    readers[x] = new MFRC522(reader_settings[x][1], reader_settings[x][0]); 
    
    //Init the reader 
    readers[x] -> PCD_Init();
    
    //Test the reader
    byte reader_version;
    reader_version = readers[x] -> PCD_ReadRegister(readers[x] -> VersionReg);
    if ((reader_version == 0x00) || (reader_version == 0xFF)) { bitWrite(au16data[2], x, 1); } //Incorrect version - probably hardware fault, put that in the register
  }
}

void record_uid(MFRC522::Uid *uid, int reader_num) {au16data[reader_settings[reader_num][2]] = (uint16_t) uid;} //Recording uid to its register in au16_data

void reset_uid(int reader_num) { au16data[reader_settings[reader_num][2]] = 0;} //Resetting the UID since no card is found on the reader

void loop() {
  slave.poll( au16data, 9 );
  au16data[0] = 0;
  au16data[1] = 0;
  for(int x = 0; x < num_readers; x++)
  { 
    readers[x] -> PICC_ReadCardSerial(); //Seems like we need two Select's in a row to detect card's presence.
    readers[x] -> PICC_IsNewCardPresent();
    if (! readers[x] -> PICC_ReadCardSerial()) //See, this does the same PICC_Select, but this one fails if there is no card on the reader, while the first doesn't. Funny. 
    {
      //Card not present 
      reset_uid(x);
    }
    else 
    {
      //Card present
      record_uid(&(readers[x] -> uid), x);
    }
  }
  au16data[6] = slave.getInCnt();
  au16data[7] = slave.getOutCnt();
  au16data[8] = slave.getErrCnt();
}


