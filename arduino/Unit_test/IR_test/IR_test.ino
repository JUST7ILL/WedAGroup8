#define IR_DPin_0 32//最左邊的IR
#define IR_DPin_1 34
#define IR_DPin_2 36
#define IR_DPin_3 38
#define IR_DPin_4 40
int PWMA = 11;
int AIN2 = 3;
int AIN1 = 2;
int BIN1 = 5;
int BIN2 = 6;
int PWMB = 12;
void setup() {
  // put your setup code here, to run once:
  pinMode(IR_DPin_0,INPUT);
  pinMode(IR_DPin_1,INPUT);
  pinMode(IR_DPin_2,INPUT);
  pinMode(IR_DPin_3,INPUT);
  pinMode(IR_DPin_4,INPUT);
  //========================================
  //=====================
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int sensorValue_0 = digitalRead(IR_DPin_0);
  int sensorValue_1 = digitalRead(IR_DPin_1);
  int sensorValue_2 = digitalRead(IR_DPin_2);
  int sensorValue_3 = digitalRead(IR_DPin_3);
  int sensorValue_4 = digitalRead(IR_DPin_4);
  Serial.print("#0:");
  Serial.println(sensorValue_0);
  Serial.print("#1:");
  Serial.println(sensorValue_1);
  Serial.print("#2:");
  Serial.println(sensorValue_2);
  Serial.print("#3:");
  Serial.println(sensorValue_3);
  Serial.print("#4:");
  Serial.println(sensorValue_4);
  delay(1000);

}
