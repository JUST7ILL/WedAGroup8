#include<SPI.h>
#include<MFRC522.h>
#define RST_PIN 9
#define SS_PIN 53

MFRC522 *mfrc522;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  SPI.begin();
  mfrc522 = new MFRC522(SS_PIN,RST_PIN);
  mfrc522->PCD_Init();
  Serial.println(F("Read UID on a MIFARE PICC:"));
}

void loop() {
  // put your main code here, to run repeatedly:
  if(!mfrc522->PICC_IsNewCardPresent()){
    goto FuncEnd;
  }
  if(!mfrc522->PICC_ReadCardSerial()){
    goto FuncEnd;
  }
  Serial.println("**Card Detected:**");
  mfrc522->PICC_DumpDetailsToSerial(&(mfrc522->uid));
  mfrc522->PICC_HaltA();
  mfrc522->PCD_StopCrypto1();
    FuncEnd:;
}
