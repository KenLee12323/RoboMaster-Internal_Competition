import cv2
import numpy as np
import time
import serial

from getkey import getkey, keys
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import json
class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return json.JSONEncoder.default(self, obj)

class NumpyDecoder(json.JSONDecoder):
	def decode(self, obj):
		data = json.JSONDecoder.decode(self, obj)
		return dict(((k, np.asarray(v)) if (isinstance(v[0], int) or isinstance(v[0], float)) else (k,v)) if isinstance(v, list) else (k,v) for k,v in data.items())
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#-----------------------Port Communication------------------------------#
def decodeUART(signal):
	return {
	1:'stop',
	3:'r',
	5:'b',
	7:'y',
	9:'g'
	}.get(signal, 'Got Another Value!')

def getSignal(com):
	while True:
		data = com.read(com.inWaiting())
		if data != b'':
			return data[-1]
#-----------------------------Motion Control-----------------------------#
def moveRight(com, signal=b'0x1'):
	com.write(b'0x1')
	print('moveRight!')
	# time.sleep(0.5) 	#??
def moveLeft(com, signal=b'0x2'):
	com.write(b'0x2')
	print('moveLeft!')
def armUp(com, signal=b'0x3'):
	com.write(b'0x3')
	print('armUp!')
def armDown(com, signal=b'0x4'):
	com.write(b'0x4')
	print('armDown!')
def armOpen(com, signal=b'0x5'):
	com.write(b'0x5')
	print('armOpen!')
def armClose(com, signal=b'0x6'):
	com.write(b'0x6')
	print('armClose!')
def positionReset(com, signal=b'0x7'):
	com.write(b'0x7')
	print('positionReset')
def getPosition(com, signal=b'0x8'):
	com.write(b'0x8')
	position = getSignal(com)
	print('getPosition: ', position)
	return position
#-----------------------------------------------------------------------#
#-------------------------Camera Comtrol--------------------------------#
def findMoment(mask, coords):
	return np.mean(coords, axis=0)[0]

def isExist(coords, area_thres=6000):
	if (coords is not None) and (len(coords)>area_thres):
		# print("len(coords): ", len(coords))
		return True
	else:
		return False

# Return: rectified mask and pixels coords
def maskNpixelsLoc(frame, lower_color, upper_color, kernel=(5,5)):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower_color, upper_color)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	coords = cv2.findNonZero(mask_color)
	return [mask, coords]

def getGoodFrame(cam, upper=100, lower=300, ratio=1, shape=(480,640,3)):
	cv2.waitKey(33)
	_, frame = cam.read()
	frame = frame[upper:lower,:]
	frame = cv2.medianBlur(frame, 5, 0) # Or cv2.GaussianBlur(frame, (5, 5), 0)
	# frame = cv2.resize(frame, (shape[0]*ratio,shape[1]*ratio))
	return frame
#-----------------------------------------------------------------------#
#-----------------------Algorithm Control-------------------------------#
def grabBox(com):
	armDown(com)
	armClose(com)
	armUp(com)
	time.sleep(0.5)
	armDown(com)
	armOpen(com)
	armUp(com)
	positionReset(com)
	return True

def option(com, mask, coords, shape=(480,640,3), dist_thres=5):
	midX, midY = shape[0]/2, shape[1]/2
	moment = findMoment(mask, coords)
	distance = moment[0]-midX
	if abs(distance)<=dist_thres:
		grabBox(com)
	elif distance>dist_thres:
		moveRight()
	else:
		moveLeft()
	return

#-----------------------------------------------------------------------#

def main():
	colors = {'r':['lower_red','upper_red'],'b':['lower_blue','upper_blue'],'g':['lower_green','upper_green'],'y':['lower_yellow','upper_yellow']}

	# load back json file #
	with open('colors_ranges.json', 'r') as fp:
		data = json.load(fp)
	data = json.loads(data,cls=NumpyDecoder)

	# init port #
	com = serial.Serial('COM8', 115200) 	#receive UART
	com1 = serial.Serial('COM9', 115200) 	#control Mining Machine
	if not com.isOpen():
		print('com port not opened!')
		exit(1)
	if not com1.isOpen():
		print('com1 port not opened!')
		exit(1)

	# init camera (480,640,3) #
	cam = cv2.VideoCapture(0)
	cv2.waitKey(33)
	_, frame = cam.read()
	frame_H, frame_W, frame_C = frame.shape

	# init mining machine #
	# ################### #

	while True:
		key = getkey(blocking=False).decode('utf-8')
		if key=='s' or key=='S':
			print("Mining Machine Starts!")
			break

	while True:
		signal = getSignal(com)
		signal = decodeUART(signal)
		if data == 'stop':
			continue
		else:
			frame = getGoodFrame(cam)
			color = colors[signal]
			[mask, pixels] = maskNpixelsLoc(frame, color[0], color[1])
			# cv2.imshow("frame", frame)
			# cv2.imshow("mask"+data, mask)
			if not isExist(pixels):
				moveRight(com1, ??)
				continue
			else:
				option(com1, mask, pixels)
				# moment = findMoment(mask, coords)
				# cv2.line(frame,(int(moment[0]),0),(int(moment[0]),200),(0,0,255),3)
	 			# cv2.imshow("frame1", frame)



if __name__ == "__main__":
	print("Auto Start")
	main()
	print("Mission Complete")