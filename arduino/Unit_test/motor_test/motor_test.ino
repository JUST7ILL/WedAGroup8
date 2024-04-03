int PWMA = 11;
int AIN2 = 3;
int AIN1 = 2;
int BIN1 = 5;
int BIN2 = 6;
int PWMB = 12;
void setup() {
  // 腳位設定
  pinMode(PWMA,OUTPUT);
  pinMode(PWMB,OUTPUT);
  //右輪
  pinMode(AIN1,OUTPUT);
  pinMode(AIN2,OUTPUT);
  //左輪
  pinMode(BIN1,OUTPUT);
  pinMode(BIN2,OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //pinMode(STBY,OUTPUT)這行不用寫，因為本來就接在5V(HIGH)上面
  digitalWrite(PWMA,HIGH);
  digitalWrite(PWMB,HIGH);
  //後退
  digitalWrite(AIN1,HIGH);
  digitalWrite(AIN2,LOW);
  digitalWrite(BIN1,HIGH);
  digitalWrite(BIN2,LOW);
  delay(1000);
  //前進
  digitalWrite(AIN1,LOW);
  digitalWrite(AIN2,HIGH);
  digitalWrite(BIN1,LOW);
  digitalWrite(BIN2,HIGH);
  delay(1000);
  //原地右轉
  digitalWrite(AIN1,HIGH);
  digitalWrite(AIN2,LOW);
  digitalWrite(BIN1,LOW);
  digitalWrite(BIN2,HIGH);
  delay(1000);
  //停
  digitalWrite(AIN1,LOW);
  digitalWrite(AIN2,LOW);
  digitalWrite(BIN1,LOW);
  digitalWrite(BIN2,LOW);
  delay(1000);
}

