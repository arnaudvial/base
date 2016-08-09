#!/usr/bin/python

import os
import time
import serial
import sys
from time import sleep

SOH = chr(0x01)
STX = chr(0x02)
EOT = chr(0x04)
ACK = chr(0x06)
NAK = chr(0x15)
CAN = chr(0x18)
CRC = chr(0x43)

DEVICE_ID="747D1"

def prepareStr(d):

        res=""
        for i in range(0,len(d),2):
                res=res+d[i:i+2]+" "
        return res.strip()


def hexToByte( hexStr ):
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )


def getc(size, timeout=1):
    return ser.read(size)

def putc(data, timeout=1):
    ser.write(data)
    sleep(0.001) # give device time to prepare new buffer and start sending it

def WaitFor(success, failure, timeOut):
    return ReceiveUntil(success, failure, timeOut) != ''

def ReceiveUntil(success, failure, timeOut):
	iterCount = timeOut / 0.1
	ser.timeout = 0.1
	currentMsg = ''
	while iterCount >= 0 and success not in currentMsg and failure not in currentMsg :
		sleep(0.1)
		while ser.inWaiting() > 0 : # bunch of data ready for reading
			c = ser.read()
			currentMsg += c
		iterCount -= 1
	if success in currentMsg :
		return currentMsg
	elif failure in currentMsg :
		print 'Failure (' + currentMsg.replace('\r\n', '') + ')'
	else :
		print 'Receive timeout (' + currentMsg.replace('\r\n', '') + ')'
	return ''

print 'Sending SigFox Message...'

# allow serial port choice from parameter - default is /dev/ttyAMA0
portName = '/dev/ttyAMA0'
if len(sys.argv) == 3:
    portName = sys.argv[2]

print 'Serial port : ' + portName

ser = serial.Serial(
	port=portName,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

if(ser.isOpen() == True): # on some platforms the serial port needs to be closed first 
    ser.close()

try:
    ser.open()
except serial.SerialException as e:
    sys.stderr.write("Could not open serial port {}: {}\n".format(ser.name, e))
    sys.exit(1)

ser.write('AT\r')
if WaitFor('OK', 'ERROR', 3) :
	print('SigFox Modem OK')

	data = format(sys.argv[1]).encode('hex')	
	ser.write("AT$SS="+data+"\r")
	print('Sending ...'+str(data))
	if WaitFor('OK', 'ERROR', 15) :
		print('OK Message sent')
	i=1
	found=False
	while (i<10):
		time.sleep(1)
		for file in os.listdir("./"):
    			if file.endswith(".sig"):
        			ff=open(file)
				recv=ff.readline()
				ff.close()
				if (recv == data):
					print "callback OK : "+hexToByte(prepareStr(str(recv)))+" "+str(i)
					os.remove(file)
					found=True
					break
		if (found):
			break	
		i=i+1
		print str(i)+" tentatives sans callback !! "		
else:
	print 'SigFox Modem Error'

ser.close()

