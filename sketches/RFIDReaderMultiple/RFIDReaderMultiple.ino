#include <SPI.h>
#include <MFRC522.h>

#define num_readers 2


MFRC522 *readers[num_readers];

//Array with configs for each reader. 
//Structure: {RST_PIN, SS_PIN}
int reader_settings[][2] = {{A1, A0},
                            {A3, A2}};

void setup() {		// Initialize serial communications with the PC
  SPI.begin();			// Init SPI bus
  Serial.begin(115200);
	setup_readers();
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
    byte v = readers[x] -> PCD_ReadRegister(readers[x] -> VersionReg);
    Serial.print(F("Init reader number "));
    Serial.println(x);
    Serial.print(F("Software Version: 0x"));
    Serial.print(v, HEX);
    if (v == 0x91)
      Serial.print(F(" = v1.0"));
    else if (v == 0x92)
      Serial.print(F(" = v2.0"));
    else
      Serial.print(F(" (unknown)"));
    Serial.println("");
    if ((v == 0x00) || (v == 0xFF)) {
      Serial.println(F("WARNING: Communication failure, is the MFRC522 properly connected?"));
    }
  }
}

//void print_uid(MFRC522::Uid *uid) {au16data[reader_settings[reader_num][2]] = (uint16_t) uid;} 

void loop() {
  for(int x = 0; x < num_readers; x++)
  { 
    if ( ! readers[x] -> PICC_IsNewCardPresent()) {
        break;
    }

    // Select one of the cards
    if ( ! readers[x] -> PICC_ReadCardSerial()) {
        break;
    }

    // Dump debug info about the card. PICC_HaltA() is automatically called.
    readers[x] -> PICC_DumpToSerial(&(readers[x] -> uid));
  }
  /*  Serial.print("UID size : ");
    Serial.println(mfrc522.uid.size);

    Serial.print("Printing HEX UID : ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  } 
  Serial.println("");

  unsigned long UID_unsigned;
  UID_unsigned =  mfrc522.uid.uidByte[0] << 24;
  UID_unsigned += mfrc522.uid.uidByte[1] << 16;
  UID_unsigned += mfrc522.uid.uidByte[2] <<  8;
  UID_unsigned += mfrc522.uid.uidByte[3];

  Serial.println();
  Serial.println("UID Unsigned int"); 
  Serial.println(UID_unsigned);

  String UID_string =  (String)UID_unsigned;
  long UID_LONG=(long)UID_unsigned;

  Serial.println("UID Long :");
  Serial.println(UID_LONG);

  Serial.println("UID String :");
  Serial.println(UID_string);*/
}

