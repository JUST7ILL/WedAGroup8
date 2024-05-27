# -*- coding: utf-8 -*-
"""
Created on Mon May 27 22:05:25 2024

@author: Yang
"""
from geopy.geocoders import Nominatim
import serial
import time
import string
import pynmea2
import json
import math
import requests

url='https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
data= requests.get(url).content.decode("utf-8")

jsondata = json.loads(data)

def distance(la1,la2,lo1,lo2):
    dis = math.sqrt((la1-la2)*(la1-la2)+(lo1-lo2)*(lo1-lo2))
    return dis
def angle(la1,la2,lo1,lo2):
    ang = math.atan((la2-la1)/(lo2-lo1))
    return ang

while True:
  port="/dev/ttyS0"
  ser=serial.Serial(port, baudrate=9600, timeout=0.5)
  dataout = pynmea2.NMEAStreamReader()
  ndata=ser.readline()
  newdata=ndata.decode('ascii')
  #print(newdata)
  if newdata[0:6] == "$GPRMC":
    newmsg=pynmea2.parse(newdata)
    now_lat=newmsg.latitude
    now_lng=newmsg.longitude
    #geolocator = Nominatim(user_agent="gps")
    #location = geolocator.reverse(str(lat)+","+str(lng))
    #print(location.address)
    #預設輸出
    f_sna=jsondata[0]["sna"]
    f_ava=jsondata[0]["available_return_bikes"]
    f_dis=distance(now_lat,jsondata[0]["latitude"],now_lng,jsondata[0]["longitude"])
    f_ang=angle(now_lat,jsondata[0]["latitude"],now_lng,jsondata[0]["longitude"])
    #尋找最近站點
    for x in jsondata:
        c_sna=x["sna"]#站點名稱
        c_ava=x["available_return_bikes"]#剩餘車位
        c_la=x["latitude"]
        c_lo=x["longitude"]
        c_dis=distance(now_lat, c_la , now_lng, c_lo)
        c_ang=angle(now_lat, c_la,now_lng,c_lo)
        if (c_dis<f_dis and c_ava>0):
            f_sna=c_sna
            f_ava=c_ava
            f_dis=c_dis
            f_ang=c_ang
    #輸出
    row='最近站點:'+f_sna+' 剩餘車位:'+str(f_ava)+' 距離:'+str(f_dis)+' 方位(東方為0度)'+str(f_ang)
    print(row)