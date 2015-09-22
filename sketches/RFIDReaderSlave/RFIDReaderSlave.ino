#include <SPI.h>
#include <Wire.h>
#include <MFRC522.h>
#define RST_PIN		A1		
#define SS_PIN		A0		

#define address 2

uint16_t xor_uid = 0;

MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance

void setup()
{
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();		// Init MFRC522
	Wire.begin(address);                // join i2c bus with address #8
  Wire.onRequest(sendCardInfo); // register event
  //mfrc522.PCD_SetAntennaGain(mfrc522.RxGain_max);
}

uint16_t read_card() {
  uint16_t xor_uid = 0;
  if (! mfrc522.PICC_ReadCardSerial()) 
    { //Okay. This does the same PICC_Select as the previous ReadCardSerial(), but this one fails if there is no card on the reader. Funny. 
      //Seems like we need two Select's in a row to detect card's presence.
      xor_uid = 0;
    }
  else 
  {    
    for (int i = 0; i < mfrc522.uid.size; i=i+2) 
    {  
      xor_uid = xor_uid ^ (mfrc522.uid.uidByte[i]<<8 | mfrc522.uid.uidByte[i+1]);
    }
  }
  return xor_uid;
}

void loop()
{
  mfrc522.PICC_ReadCardSerial(); //Always fails
  mfrc522.PICC_IsNewCardPresent(); //Does RequestA 
  xor_uid = read_card();
  delay(1);
}

void sendCardInfo() {
  byte myArray[2]; //Thanks http://thewanderingengineer.com/2015/05/06/sending-16-bit-and-32-bit-numbers-with-arduino-i2c for this solution
  myArray[0] = (xor_uid >> 8) & 0xFF;
  myArray[1] = xor_uid & 0xFF;
  Wire.write(myArray, 2);
}
