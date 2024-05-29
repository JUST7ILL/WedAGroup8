import time
import RPi.GPIO as GPIO

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