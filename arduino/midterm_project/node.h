/***************************************************************************/
// File			  [node.h]
// Author		  [Erik Kuo, Joshua Lin]
// Synopsis		[Code for managing car movement when encounter a node]
// Functions  [/* add on your own! */]
// Modify		  [2020/03/027 Erik Kuo]
/***************************************************************************/

#include "track.h"
#include "bluetooth.h"
#include "RFID.h"
/*===========================import variable===========================*/
int extern _Tp;
int extern turn_speed;
int extern l2, l1, m0, r1, r2;
/*===========================import variable===========================*/

// TODO: add some function to control your car when encounter a node
// here are something you can try: left_turn, right_turn... etc.

void readIRs();
void straight();
void turn_left();
void turn_right();

void ReadIRs(){
  l2 = digitalRead(IRpin_LL);
  l1 = digitalRead(IRpin_L);
  m0 = digitalRead(IRpin_M);
  r1 = digitalRead(IRpin_R);
  r2 = digitalRead(IRpin_RR);
}

byte* _id;
byte _idSize;

void straight(){
  ReadIRs();
  while(l2&&l1&&m0&&r1&&r2){ // 走出出發點
    _id = rfid(_idSize);
    if(_id != 0){
      send_msg('r');
      send_byte(_id, _idSize);
      return;
    }
    tracking(l2, l1, m0, r1, r2);
    ReadIRs();
  }
  while((l2&&l1&&m0&&r1&&r2) == 0){ // 在路上
    _id = rfid(_idSize);
    if(_id != 0){
      send_msg('r');
      send_byte(_id, _idSize);
      return;
    }
    tracking(l2, l1, m0, r1, r2);
    ReadIRs();
  }
  while(l2&&l1&&m0&&r1&&r2){ // 走進目標點
    _id = rfid(_idSize);
    if(_id != 0){
      send_msg('r');
      send_byte(_id, _idSize);
      return;
    }
    tracking(l2, l1, m0, r1, r2);
    ReadIRs();
  }
  delay(30000/_Tp);
  send_msg('n');
}

void turn_left(){
  ReadIRs();
  MotorWriting(-turn_speed, turn_speed);
  while(l2||l1||m0){ // 轉出黑線
    ReadIRs();
  }
  delay(20000/turn_speed); // 確保轉出黑線
  ReadIRs();
  while(m0 == 0 && r1 == 0){ // 偵測到左側黑線停止
    ReadIRs();
  }
  send_msg('n');
}

void turn_right(){
  ReadIRs();
  MotorWriting(turn_speed, -turn_speed);
  while(r2||r1||m0){ // 轉出黑線
    ReadIRs();
  }
  delay(20000/turn_speed); // 確保轉出黑線
  ReadIRs();
  while(m0 == 0 && l1 == 0){ // 偵測到左側黑線停止
    ReadIRs();
  }
  send_msg('n');
}