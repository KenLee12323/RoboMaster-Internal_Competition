# coding = UTF-8
import serial
import time

#mimmic board
com = serial.Serial('COM8')
#mimmic laptop
com1 = serial.Serial('COM9')

try:
	while True:
		data = com.read(com.inWaiting())
		data1 = com1.read(com1.inWaiting())
		if data == b'':
			print('Board: ','got nothing, send me sth!')
			time.sleep(0.5)
			com.write(b'got nothing, send me sth!')
		if data1 != b'':
			print('Laptop: ', 'got from board')
			com1.write(b'send you sth la')
			time.sleep(0.5)
except:
	pass