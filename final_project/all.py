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
import RPi.GPIO as GPIO
import numpy as np

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
PIN_D0 = 16
PIN_D1 = 17
PIN_D2 = 22
PIN_D3 = 23
PIN_D4 = 24
PIN_D5 = 25
PIN_D6 = 26
PIN_D7 = 6
PIN_RS = 8
PIN_RW = 10
PIN_E = 11

def outputD(num):
	GPIO.output(PIN_D7, (num//128))
	GPIO.output(PIN_D6, (num%128//64))
	GPIO.output(PIN_D5, (num%64//32))
	GPIO.output(PIN_D4, (num%32//16))
	GPIO.output(PIN_D3, (num%16//8))
	GPIO.output(PIN_D2, (num%8//4))
	GPIO.output(PIN_D1, (num%4//2))
	GPIO.output(PIN_D0, (num%2))
	time.sleep(0.001)
	GPIO.output(PIN_E, True)
	time.sleep(0.001)
	GPIO.output(PIN_E, False)
	time.sleep(0.001)

def resetGDRAM():
	for i in range(64):
		for j in range(16):
			GPIO.output(PIN_RS, False)
			outputD(0x34)
			outputD(128+i%32)
			outputD(128+j)
			outputD(0x30)
			GPIO.output(PIN_RS, True)
			GPIO.output(PIN_D7, 0)
			GPIO.output(PIN_D6, 0)
			GPIO.output(PIN_D5, 0)
			GPIO.output(PIN_D4, 0)
			GPIO.output(PIN_D3, 0)
			GPIO.output(PIN_D2, 0)
			GPIO.output(PIN_D1, 0)
			GPIO.output(PIN_D0, 0)
			time.sleep(0.001)
			GPIO.output(PIN_E, True)
			time.sleep(0.001)
			GPIO.output(PIN_E, False)
			time.sleep(0.001)
			GPIO.output(PIN_D7, 0)
			GPIO.output(PIN_D6, 0)
			GPIO.output(PIN_D5, 0)
			GPIO.output(PIN_D4, 0)
			GPIO.output(PIN_D3, 0)
			GPIO.output(PIN_D2, 0)
			GPIO.output(PIN_D1, 0)
			GPIO.output(PIN_D0, 0)
			time.sleep(0.001)
			GPIO.output(PIN_E, True)
			time.sleep(0.001)
			GPIO.output(PIN_E, False)
			time.sleep(0.001)
		
	

def get_arrow(n):
	if n == 0:
		return np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
	elif n == 1:
		return np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
	elif n == 2:
		return np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
	elif n <= 4:
		ar = get_arrow(4-n)
		aw = np.zeros([32,32])
		for i in range(32):
			for j in range(32):
				aw[i][j] = ar[31-j][31-i]
		return aw
	elif n <= 8:
		ar = get_arrow(8-n)
		aw = np.zeros([32,32])
		for i in range(32):
			for j in range(32):
				aw[i][j] = ar[31-i][j]
		return aw
	elif n <= 15:
		ar = get_arrow(16-n)
		aw = np.zeros([32,32])
		for i in range(32):
			for j in range(32):
				aw[i][j] = ar[i][31-j]
		return aw
		

def draw_arrow(n):
	ar = get_arrow(n)
	for i in range(32):
		GPIO.output(PIN_RS, False)
		outputD(0x34)
		outputD(128+i)
		outputD(128+14)
		outputD(0x30)
		GPIO.output(PIN_RS, True)
		GPIO.output(PIN_D7, int(ar[i][0]))
		GPIO.output(PIN_D6, int(ar[i][1]))
		GPIO.output(PIN_D5, int(ar[i][2]))
		GPIO.output(PIN_D4, int(ar[i][3]))
		GPIO.output(PIN_D3, int(ar[i][4]))
		GPIO.output(PIN_D2, int(ar[i][5]))
		GPIO.output(PIN_D1, int(ar[i][6]))
		GPIO.output(PIN_D0, int(ar[i][7]))
		time.sleep(0.001)
		GPIO.output(PIN_E, True)
		time.sleep(0.001)
		GPIO.output(PIN_E, False)
		time.sleep(0.001)
		GPIO.output(PIN_D7, int(ar[i][8]))
		GPIO.output(PIN_D6, int(ar[i][9]))
		GPIO.output(PIN_D5, int(ar[i][10]))
		GPIO.output(PIN_D4, int(ar[i][11]))
		GPIO.output(PIN_D3, int(ar[i][12]))
		GPIO.output(PIN_D2, int(ar[i][13]))
		GPIO.output(PIN_D1, int(ar[i][14]))
		GPIO.output(PIN_D0, int(ar[i][15]))
		time.sleep(0.001)
		GPIO.output(PIN_E, True)
		time.sleep(0.001)
		GPIO.output(PIN_E, False)
		time.sleep(0.001)
		GPIO.output(PIN_D7, int(ar[i][16]))
		GPIO.output(PIN_D6, int(ar[i][17]))
		GPIO.output(PIN_D5, int(ar[i][18]))
		GPIO.output(PIN_D4, int(ar[i][19]))
		GPIO.output(PIN_D3, int(ar[i][20]))
		GPIO.output(PIN_D2, int(ar[i][21]))
		GPIO.output(PIN_D1, int(ar[i][22]))
		GPIO.output(PIN_D0, int(ar[i][23]))
		time.sleep(0.001)
		GPIO.output(PIN_E, True)
		time.sleep(0.001)
		GPIO.output(PIN_E, False)
		time.sleep(0.001)
		GPIO.output(PIN_D7, int(ar[i][24]))
		GPIO.output(PIN_D6, int(ar[i][25]))
		GPIO.output(PIN_D5, int(ar[i][26]))
		GPIO.output(PIN_D4, int(ar[i][27]))
		GPIO.output(PIN_D3, int(ar[i][28]))
		GPIO.output(PIN_D2, int(ar[i][29]))
		GPIO.output(PIN_D1, int(ar[i][30]))
		GPIO.output(PIN_D0, int(ar[i][31]))
		time.sleep(0.001)
		GPIO.output(PIN_E, True)
		time.sleep(0.001)
		GPIO.output(PIN_E, False)
		time.sleep(0.001)
	ClearAll()
	GPIO.output(PIN_RS, False)
	outputD(0x34)
	outputD(0x36)
	outputD(0x30)
	GPIO.output(PIN_RS, True)
			
def SetLine(n): # from 1 to 4
	lines = [0x80, 0x90, 0x88, 0x98]
	GPIO.output(PIN_RS, False)
	outputD(lines[n-1])
	
def ClearAll():
	GPIO.output(PIN_RS, False)
	outputD(1)
	time.sleep(0.05)
	

def WriteWords(data, line):
	half_count = 0
	line_length = 0 # for automatic line transfer
	GPIO.output(PIN_RS, True)
	for c in data:
		b = c.encode('big5')
		if len(b) == 1:
			half_count += 1
		else:
			if half_count % 2 == 1:
				outputD(32) # add space
				line_length += 1
			half_count = 0
		if line_length >= 16:
			line += 1
			SetLine(line)
			GPIO.output(PIN_RS, True)
			line_length = 0
		line_length += len(b)
		for i in b:
			outputD(i)
	if half_count % 2 == 1:
		outputD(32) # add space

#web
url='https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
data= requests.get(url).content.decode("utf-8")

jsondata = json.loads(data)
#some function
def angle(lat1, lat2, lon1, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(d_lon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

def distance(lat1, lat2, lon1, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    R = 6371000.0
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = math.sin(d_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dis = R * c
    return dis

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
		
# initialize LCD
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_D0, GPIO.OUT)
GPIO.setup(PIN_D1, GPIO.OUT)
GPIO.setup(PIN_D2, GPIO.OUT)
GPIO.setup(PIN_D3, GPIO.OUT)
GPIO.setup(PIN_D4, GPIO.OUT)
GPIO.setup(PIN_D5, GPIO.OUT)
GPIO.setup(PIN_D6, GPIO.OUT)
GPIO.setup(PIN_D7, GPIO.OUT)
GPIO.setup(PIN_RS, GPIO.OUT)
GPIO.setup(PIN_RW, GPIO.OUT)
GPIO.setup(PIN_E, GPIO.OUT)

GPIO.output(PIN_E, False)
GPIO.output(PIN_RW, False)
GPIO.output(PIN_RS, False) # command
time.sleep(0.05)
outputD(48)
outputD(48)
outputD(12)
outputD(1)
time.sleep(0.05)
outputD(6)
# end of init LCD

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
    if float(now_lat) > 26 or float(now_lat) < 21 or float(now_lng) > 123 or float(now_lng) < 119:
        continue
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
    arrow_angle = (heading_angle-f_ang_gps) % 360
    # row='最近站點:'+f_sna+' 剩餘車位:'+str(f_ava)+' 距離:'+str(f_dis)+' GPS方位(N為0度)'+str(f_ang_gps)+' heading angle:'+str(heading_angle)+' 夾角:'+str((heading_angle-f_ang_gps) % 360)
    # print(row)
    draw_arrow((arrow_angle + 22.5/2) // 16)
    WriteWords(f_sna[11:], 1)
    WriteWords(str(int(f_dis)) + 'm', 4)
    time.sleep(1)
    
    
