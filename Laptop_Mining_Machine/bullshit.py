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

def moveRight():
	print('Move Right!')
def moveLeft():
	print('Move Left!')
def positionReset():
	print('Position Reset')


# return moment: array([x,y])
def findMoment(mask, coords):
	return np.mean(coords, axis=0)[0]

def assureCBox(coords, area_thres=6000):
	if (coords is not None) and (len(coords)>area_thres):
		print("len(coords): ", len(coords))
		return True
	else:
		return False

# mask_place=np.array([255,255,255],dtype=np.uint8)
# np_mask_color = np.array(mask_color)
# Return: rectified mask and pixels coords
def maskNpixelsLoc(hsv, lower_color, upper_color, kernel=(5,5)):
	mask_color = cv2.inRange(hsv, lower_color, upper_color)
	mask_color = cv2.morphologyEx(mask_color, cv2.MORPH_OPEN, kernel)
	coords = cv2.findNonZero(mask_color)
	return [mask_color, coords]

### do frame-wise box matching inside this function alone is faster ###
### since only care one color box 									###
def grab(cam, color, moment, lower_range, upper_range, frame_W, tolerance=5, adjust=10):
	frame_WMid = frame_W/2 + adjust			# need not to floor
	distance = moment[0]-frame_WMid
	last_act = None
	missed = 0
	while abs(distance)>tolerance:
		if distance>0:
			moveRight()
			last_act = 'R'
		else:
			moveLeft()
			last_act = 'L'


		cv2.waitKey(33)
		_, frame = cam.read()
		############################################
		### any preprocessing? Or Cut Upper/Bottom img? ###
		frame = frame[100:300,:]
		# frame = cv2.resize(frame, (160,120))
		frame = cv2.medianBlur(frame, 5, 0) # Or cv2.GaussianBlur(frame, (5, 5), 0)
		############################################
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		[mask, coords] = maskNpixelsLoc(hsv,lower_range, upper_range)
		if not assureCBox(coords):
			missed+=1
			if missed>=3:							# Cannot find for how many time?
				print("Suddenly Blinded!")
				time.sleep(5)
				return False
			else:
				moveRight() if last_act=='R' else moveLeft()
		else:
			missed=0
			moment = findMoment(mask, coords)
			distance = moment[0]-frame_WMid
		
		print("Moment, Distance, frame_WMid: ", moment, distance, frame_WMid)
		cv2.line(frame,(int(moment[0]),0),(int(moment[0]),200),(0,0,255),3)
		cv2.imshow("Frame", frame)
		cv2.imshow("Mask", mask)

	print("Now Grabbing Box ", color, " at pixel-distance: ", distance)
	### Do grabbing ###
	time.sleep(5)
	return True

def main():
	range_dict = {'r':['lower_red','upper_red'],'b':['lower_blue','upper_blue'],'g':['lower_green','upper_green'],'y':['lower_yellow','upper_yellow']}
	# load back json file # #
	with open('colors_ranges.json', 'r') as fp:
		data = json.load(fp)
	data = json.loads(data,cls=NumpyDecoder)
	# print(data)

	cam = cv2.VideoCapture(0)
	cv2.waitKey(33)
	_, frame = cam.read()
	# laptop and provided cam: (480,640,3)
	frame_H, frame_W, frame_C = frame.shape	
	# print(frame.shape)
	# time.sleep(5)
	# frame_H, frame_W = frame_H/4, frame_W/4 #<<-cannot be too small to match midt-pt

	while True:
		while True:
			key = getkey(blocking=False).decode('utf-8')
			if key=='s' or key=='S':
				print("Grab box starts!")
				break
			elif key=='l' or key=='L':
				print("Grab box ends!")
				exit(0)

		grabbed = {'r':False,'b':False,'g':False,'y':False}
		while True:
			key = getkey(blocking=False).decode('utf-8')
			if key=='q' or key=='Q':
				print('Manual Exits')
				positionReset()
				break
			if grabbed['r'] and grabbed['b'] and grabbed['g'] and grabbed['y']:
				print('All boxes grabbed!')
				positionReset()
				break

			cv2.waitKey(33)
			_, frame = cam.read()
			############################################
			### any resize? Or Cut Upper/Bottom img? ###
			frame = frame[100:300,:]
			# frame = cv2.resize(frame, (160,120))
			frame = cv2.medianBlur(frame, 5, 0) # Or cv2.GaussianBlur(frame, (5, 5), 0)
			############################################
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			[mask_red, reds] = maskNpixelsLoc(hsv, data[range_dict['r'][0]], data[range_dict['r'][1]])
			[mask_blue, blues] = maskNpixelsLoc(hsv, data[range_dict['b'][0]], data[range_dict['b'][1]])
			[mask_green, greens] = maskNpixelsLoc(hsv, data[range_dict['g'][0]], data[range_dict['g'][1]])
			[mask_yellow, yellows] = maskNpixelsLoc(hsv, data[range_dict['y'][0]], data[range_dict['y'][1]])

			cv2.imshow("frame", frame)
			cv2.imshow("mask_red", mask_red)
			cv2.imshow("mask_blue", mask_blue)
			cv2.imshow("mask_green", mask_green)
			cv2.imshow("mask_yellow", mask_yellow)

			# to assure certain color boxs are in this frame #
			exists = {'r':False,'b':False,'g':False,'y':False}
			exists['r'], exists['b'], exists['g'], exists['y'] = assureCBox(reds), assureCBox(blues), assureCBox(greens), assureCBox(yellows)

			# if no box found, move right and re-do 
			if not (exists['r'] or exists['b'] or exists['g'] or exists['y']):
				### Since don't know the range for actuator now 			 ###
				### Just perform left-most search to right as initialization ###
				moveRight()
				continue

			# if boxes found, adjust position
			# sort boxes by moment x-axis in current frame #
			moments = []
			if exists['r']:
				moments.append(('r',findMoment(mask_red, reds)))
			if exists['b']:
				moments.append(('b',findMoment(mask_blue, blues)))
			if exists['g']:
				moments.append(('g',findMoment(mask_green, greens)))
			if exists['y']:
				moments.append(('y',findMoment(mask_yellow, yellows)))
			moments = sorted(moments, key=lambda x: x[1][0])
			print("Moments: ", moments)

			boxes_grabbed = True
			for moment in moments:
				if grabbed[moment[0]]==False:
					boxes_grabbed = False
					break
			if boxes_grabbed==True:
				moveRight()
				continue

			# perform  left-most grabbing #
			for moment in moments:
				if not grabbed[moment[0]]:
					print("Attempting to Grab: ", moment[0])
					time.sleep(3)
					color_range = range_dict[moment[0]]
					grabbed[moment[0]] = grab(cam, moment[0], moment[1], data[color_range[0]], data[color_range[1]], frame_W)	#moment = ('r', x-axis center point)
					break

	cam.release()
	cv2.destroyAllWindows()



if __name__ == "__main__":
	print("Auto Start")
	main()
	print("Mission Complete")