# -*- coding: utf-8 -*-
"""
Created on Fri May 10 02:28:59 2024

@author: Yang
"""

import json
import math
import requests

url='https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
data= requests.get(url).content.decode("utf-8")

jsondata = json.loads(data)

def distance(la1,la2,lo1,lo2):
    dis = math.sqrt((la1-la2)*(la1-la2)+(lo1-lo2)*(lo1-lo2))
    return dis
#醉月湖中涼亭座標 
 #緯度
fakela=25.020428317272014
 #經度
fakelo=121.53763564617941
#預設輸出
f_sna=jsondata[0]["sna"]
f_ava=jsondata[0]["available_return_bikes"]
f_dis=distance(fakela,jsondata[0]["latitude"],fakelo,jsondata[0]["longitude"])
#尋找最近站點
for x in jsondata:
    c_sna=x["sna"]#站點名稱
    c_ava=x["available_return_bikes"]#剩餘車位
    c_la=x["latitude"]
    c_lo=x["longitude"]
    c_dis=distance(fakela, c_la , fakelo, c_lo)
    if (c_dis<f_dis):
        f_sna=c_sna
        f_ava=c_ava
        f_dis=c_dis
#輸出
row='最近站點:'+f_sna+' 剩餘車位:'+str(f_ava)+' 距離:'+str(f_dis)
print(row)
        