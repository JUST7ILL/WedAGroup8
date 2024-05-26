import RPi.GPIO as GPIO
import time

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

def SetLine(n): # from 1 to 4
	lines = [0x80, 0x90, 0x88, 0x98]
	GPIO.output(PIN_RS, False)
	outputD(lines[n-1])
	
def ClearAll():
	GPIO.output(PIN_RS, False)
	outputD(1)
	time.sleep(0.05)
	

def WriteWords(data):
	GPIO.output(PIN_RS, True)
	for c in data:
		b = c.encode('big5')
		for i in b:
			outputD(i)

# initialize
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
# end of init

SetLine(1)
WriteWords(u"檔案已儲存檔案已")
SetLine(2)
WriteWords(u"儲存檔案已儲存")
time.sleep(3)
ClearAll()

GPIO.cleanup()







