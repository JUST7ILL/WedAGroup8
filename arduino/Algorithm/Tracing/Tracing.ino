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

double w0=-2.0,
  w1=-1.0,
  w2=0,
  w3=1.0,
  w4=2.0;

void ReadIRs(int& sv0, int& sv1, int& sv2, int& sv3, int& sv4){
  sv0 = digitalRead(IR_DPin_0);
  sv1 = digitalRead(IR_DPin_1);
  sv2 = digitalRead(IR_DPin_2);
  sv3 = digitalRead(IR_DPin_3);
  sv4 = digitalRead(IR_DPin_4);
}
void MotorWriting(double vL,double vR){
  if(vR>=0){
    digitalWrite(AIN1,LOW);
    digitalWrite(AIN2,HIGH);
  }
  else{
    digitalWrite(AIN1,HIGH);
    digitalWrite(AIN2,LOW);
    vR=-vR;
  }
  if(vL>=0){
    digitalWrite(BIN1,LOW);
    digitalWrite(BIN2,HIGH);
  }
  else{
    digitalWrite(BIN1,HIGH);
    digitalWrite(BIN2,LOW);
    vL=-vL;
  }
  analogWrite(PWMA,vR);
  analogWrite(PWMB,vL);

}
void Tracing(int v0,int v1,int v2, int v3, int v4){
  if(v0+v1+v2+v3+v4==0){
    MotorWriting(150, 150);
  }
  else{
    double d=(v0*w0+v1*w1+v2*w2+v3*w3+v4*w4)/(v0+v1+v2+v3+v4);
    MotorWriting(150+d*50,150-d*50);
  }
}
void straight(){
  int sv0 = 0, sv1 = 0, sv2 = 0, sv3 = 0, sv4 = 0;
  ReadIRs(sv0, sv1, sv2, sv3, sv4);
  while(sv1&&sv2&&sv3&&sv4&&sv0){ // 走出出發點
    Tracing(sv0,sv1,sv2,sv3,sv4);
    ReadIRs(sv0, sv1, sv2, sv3, sv4);
  }
  while((sv0&&sv1&&sv2&&sv3&&sv4) == 0){ // 在路上
    Tracing(sv0,sv1,sv2,sv3,sv4);
    ReadIRs(sv0, sv1, sv2, sv3, sv4);
  }
  while(sv1&&sv2&&sv3&&sv4&&sv0){ // 走進目標點
    Tracing(sv0,sv1,sv2,sv3,sv4);
    ReadIRs(sv0, sv1, sv2, sv3, sv4);
  }
  delay(200);
}

void turn_left(){
  int sv2 = digitalRead(IR_DPin_2);
  MotorWriting(-100,100); // 助教說不要轉太快
  while(sv2){ // 轉出黑線
    sv2 = digitalRead(IR_DPin_2);
  }
  delay(200); // 確保轉出黑線
  int sv3 = digitalRead(IR_DPin_3); // 避免中央沒偵測到
  while(sv2 == 0 && sv3 == 0){ // 偵測到左側黑線停止
    sv2 = digitalRead(IR_DPin_2);
    sv3 = digitalRead(IR_DPin_3);
  }
}
void turn_right(){
  int sv2 = digitalRead(IR_DPin_2);
  MotorWriting(100,-100); // 助教說不要轉太快
  while(sv2){ // 轉出黑線
    sv2 = digitalRead(IR_DPin_2);
  }
  delay(200); // 確保轉出黑線
  int sv1 = digitalRead(IR_DPin_1); // 避免中央沒偵測到
  while(sv2 == 0 && sv1 == 0){ // 偵測到右側黑線停止
    sv1 = digitalRead(IR_DPin_1);
    sv2 = digitalRead(IR_DPin_2);
  }
}

void setup() {
  pinMode(IR_DPin_0,INPUT);
  pinMode(IR_DPin_1,INPUT);
  pinMode(IR_DPin_2,INPUT);
  pinMode(IR_DPin_3,INPUT);
  pinMode(IR_DPin_4,INPUT);
//==========================
  pinMode(PWMA,OUTPUT);
  pinMode(PWMB,OUTPUT);
  //右輪
  pinMode(AIN1,OUTPUT);
  pinMode(AIN2,OUTPUT);
  //左輪
  pinMode(BIN1,OUTPUT);
  pinMode(BIN2,OUTPUT);
//==============================
  Serial.begin(115200);
  //=======================
  MotorWriting(0,0);
  straight();
  turn_left();
  straight();
  turn_left();
  straight();
  straight();
  turn_right();
  straight();
  turn_right();
  straight();
}

void loop() {
  // int sv0 = digitalRead(IR_DPin_0);
  // int sv1 = digitalRead(IR_DPin_1);
  // int sv2 = digitalRead(IR_DPin_2);
  // int sv3 = digitalRead(IR_DPin_3);
  // int sv4 = digitalRead(IR_DPin_4);
  //算誤差
  // Tracing(sv0,sv1,sv2,sv3,sv4);
  MotorWriting(0, 0);
  delay(100000);
}