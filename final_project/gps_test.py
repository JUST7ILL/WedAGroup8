from geopy.geocoders import Nominatim
import serial
import time
import string
import pynmea2

while True:
  port="/dev/ttyS0"
  ser=serial.Serial(port, baudrate=9600, timeout=0.5)
  dataout = pynmea2.NMEAStreamReader()
  ndata=ser.readline()
  newdata=ndata.decode('ascii')
  #print(newdata)
  if newdata[0:6] == "$GPRMC":
    newmsg=pynmea2.parse(newdata)
    lat=newmsg.latitude
    lng=newmsg.longitude
    #geolocator = Nominatim(user_agent="gps")
    print(str(lat)+","+str(lng))
    #location = geolocator.reverse(str(lat)+","+str(lng))
    #print(location.address)
