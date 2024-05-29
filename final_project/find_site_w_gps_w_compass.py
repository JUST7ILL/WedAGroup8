# -*- coding: utf-8 -*-
"""
Created on Mon May 27 22:05:25 2024

@author: Yang
"""
from geopy.geocoders import Nominatim
from time import sleep 
import smbus		
import serial
import time
import string
import pynmea2
import json
import math
import requests

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x1e   # HMC5883L magnetometer device address

#some MPU6050 Registers and their Address
Register_A     = 0              #Address of Configuration register A
Register_B     = 0x01           #Address of configuration register B
Register_mode  = 0x02           #Address of mode register

X_axis_H    = 0x03              #Address of X-axis MSB data register
Z_axis_H    = 0x05              #Address of Z-axis MSB data register
Y_axis_H    = 0x07              #Address of Y-axis MSB data register
declination = 0              #define declination angle of location where measurement going to be done
pi          = 3.14159265359     #define pi value

#web
url='https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
data= requests.get(url).content.decode("utf-8")

jsondata = json.loads(data)
#some function
def distance(la1,la2,lo1,lo2):
    dis = math.sqrt((la1-la2)*(la1-la2)+(lo1-lo2)*(lo1-lo2))
    return dis
def angle(la1,la2,lo1,lo2):#正東方為零度
    ang = int(math.atan((la2-la1)/(lo2-lo1))*180/pi)
    return ang

def Magnetometer_Init():
        #write to Configuration Register A
        bus.write_byte_data(Device_Address, Register_A, 0x70)

        #Write to Configuration Register B for gain
        bus.write_byte_data(Device_Address, Register_B, 0xa0)

        #Write to mode Register for selecting mode
        bus.write_byte_data(Device_Address, Register_mode, 0)
	
def read_raw_data(addr):
    
        #Read raw 16-bit value
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from module
        if(value > 32768):
            value = value - 65536
        return value

Magnetometer_Init()     # initialize HMC5883L magnetometer 

while True:
  port="/dev/ttyS0"
  ser=serial.Serial(port, baudrate=9600, timeout=0.5)
  dataout = pynmea2.NMEAStreamReader()
  newdata=ser.readline()
  #print(newdata)
  if newdata[0:6] == b"$GPRMC":
    ndata=newdata.decode('ascii')
    newmsg=pynmea2.parse(ndata)
    now_lat=newmsg.latitude
    now_lng=newmsg.longitude
    #geolocator = Nominatim(user_agent="gps")
    #location = geolocator.reverse(str(now_lat)+","+str(now_lng))
    #print(location.address)
    
    #讀羅盤
    x = read_raw_data(X_axis_H)
    z = read_raw_data(Z_axis_H)
    y = read_raw_data(Y_axis_H)
    heading = math.atan2(y, x) + declination
    
    #Due to declination check for >360 degree
    if(heading > 2*pi):
            heading = heading - 2*pi
    
    #check for sign
    if(heading < 0):
            heading = heading + 2*pi
    
    #convert into angle
    heading_angle = int(heading * 180/pi)
    
    #預設輸出
    f_sna=jsondata[0]["sna"]
    f_ava=jsondata[0]["available_return_bikes"]
    f_dis=distance(now_lat,jsondata[0]["latitude"],now_lng,jsondata[0]["longitude"])
    f_ang_gps=angle(now_lat,jsondata[0]["latitude"],now_lng,jsondata[0]["longitude"])
    
    #尋找最近站點
    for x in jsondata:
        c_sna=x["sna"]#站點名稱
        c_ava=x["available_return_bikes"]#剩餘車位
        c_la=x["latitude"]
        c_lo=x["longitude"]
        c_dis=distance(now_lat, c_la , now_lng, c_lo)
        c_ang_gps=angle(now_lat, c_la,now_lng,c_lo)
        if (c_dis<f_dis and c_ava>0):
            f_sna=c_sna
            f_ava=c_ava
            f_dis=c_dis
            f_ang_gps=c_ang_gps
    #輸出
    n_f_ang_gps = (450 - f_ang_gps) % 360 # north clockwise
    row='最近站點:'+f_sna+' 剩餘車位:'+str(f_ava)+' 距離:'+str(f_dis)+' GPS方位(N為0度)'+str(n_f_ang_gps)+' heading angle:'+str(heading_angle)+' 夾角:'+str((heading_angle-n_f_ang_gps) % 360)
    print(row)
