/***************************************************************************/
// File			  [track.h]
// Author		  [Erik Kuo]
// Synopsis		[Code used for tracking]
// Functions  [MotorWriting, MotorInverter, tracking]
// Modify		  [2020/03/27 Erik Kuo]
/***************************************************************************/

/*if you have no idea how to start*/
/*check out what you have learned from week 1 & 6*/
/*feel free to add your own function for convenience*/

/*===========================import variable===========================*/
int extern _Tp;
/*===========================import variable===========================*/

// Write the voltage to motor.
void MotorWriting(double vL, double vR) {
  if(vR>=0){
    digitalWrite(MotorR_I1,LOW);
    digitalWrite(MotorR_I2,HIGH);
  }
  else{
    digitalWrite(MotorR_I1,HIGH);
    digitalWrite(MotorR_I2,LOW);
    vR=-vR;
  }
  if(vL>=0){
    digitalWrite(MotorL_I3,LOW);
    digitalWrite(MotorL_I4,HIGH);
  }
  else{
    digitalWrite(MotorL_I3,HIGH);
    digitalWrite(MotorL_I4,LOW);
    vL=-vL;
  }
  analogWrite(MotorR_PWMR,vR);
  analogWrite(MotorL_PWML,vL);
}  // MotorWriting

// Handle negative motor_PWMR value.
void MotorInverter(int motor, bool& dir) {
    // Hint: the value of motor_PWMR must between 0~255, cannot write negative value.
}  // MotorInverter

// P/PID control Tracking
void tracking(int l2, int l1, int m0, int r1, int r2) {
    // TODO: find your own parameters!
    double _w0 = 0;  //
    double _w1 = -1.0;  //
    double _w2 = -2.0;  //
    double _Kp = 50;  // p term parameter
    double _Kd;  // d term parameter (optional)
    double _Ki;  // i term parameter (optional) (Hint: 不要調太大)
    double error = l2 * _w2 + l1 * _w1 + m0 * _w0 + r1 * (-_w1) + r2 * (-_w2);
    double vR, vL;  // 馬達左右轉速原始值(從PID control 計算出來)。Between -255 to 255.
    double adj_R = 1, adj_L = 1;  // 馬達轉速修正係數。MotorWriting(_Tp,_Tp)如果歪掉就要用參數修正。
    double sigma_IR = l2 + l1 + m0 + r1 + r2;
    // TODO: complete your P/PID tracking code
    if(sigma_IR == 0){
        vL = _Tp;
        vR = _Tp;
    }
    else{
        vL = _Tp + error * _Kp / sigma_IR;
        vR = _Tp - error * _Kp / sigma_IR;
    }
    // end TODO
    MotorWriting(adj_L * vL, adj_R * vR);
}  // tracking
