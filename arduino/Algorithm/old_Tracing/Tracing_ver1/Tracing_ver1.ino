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
  //Serial.begin(9600);
  //=======================
  MotorWriting(200,200);
  
}

void loop() {
  int sv0 = digitalRead(IR_DPin_0);
  int sv1 = digitalRead(IR_DPin_1);
  int sv2 = digitalRead(IR_DPin_2);
  int sv3 = digitalRead(IR_DPin_3);
  int sv4 = digitalRead(IR_DPin_4);
  //算誤差
  if(sv0+sv1+sv2+sv3+sv4==0){
    MotorWriting(150, 150);
  }
  else{
    double d=(sv0*w0+sv1*w1+sv2*w2+sv3*w3+sv4*w4)/(sv0+sv1+sv2+sv3+sv4);
    MotorWriting(150+d*50,150-d*50);
  }
  
}
