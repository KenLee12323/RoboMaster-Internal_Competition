# def detectColor():
#     pass

# while ser.open():
#     img = ser.read(#size of an img))
#     imshow(img)
#     
### This program performs location matching  ###
###           ###
### KenLee1223 10/28/2019                                         ###
#     
import cv2
import numpy as np
import time
import serial
from getkey import getkey, keys


command2Send = {'Up':1,'Down':2,'Left':3,'Right':4}

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

def resPosition():
	pass

def boxLocation(mask):
    nms
    x_max
    fuzzy
    medium

def colorSearch(img, lower_range, upper_range):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, lower_range, upper_range)    # mask

def arrived(img, lower_range, upper_range, threshold):
    img = colorSearch(img, lower_range, upper_range)
    no_pixel = 
    if 
    return car

def rotate(ser, deg=90):
    ser.write()
    start = time.monotomic()
    while True:
        if ser.readline().decode('asii') == 'd': #d:=done
            return True
        elif time.monotomic()-start>10:          # what if wait for 10sec and condition fail
            resPosition()
            return False

def main():
    # load back json file # #
    with open('colors_ranges.json', 'r') as fp:
        data = json.load(fp)
    color_ranges = json.loads(data,cls=NumpyDecoder)
    
    # go to the device manager and see what com port your usb to serial adaptor is using.
    # eg ser = serial.Serial('COM1', 9600)
    ser = serial.Serial('COM3',4800,8,'n',1,timeout=100)

    cam = cv2.VideoCapture(0)
    lower_circle, upper_circle = color_ranges['lower_circle'], color_ranges['upper_circle']
    while True:
        _, img = cam.read()
        cv2.waitKey(33)
        key = getkey(blocking=False).decode('utf-8')
        if key =='q' or key =='Q':
            break
        if arrived(img, lower_circle, lower_circle)
            R = rotate(ser, 90)          # what to do if rotation fail
            
            box_seq = ['r','b','g','y']
            loaded = {'r':False,'b':False,'g':False,'y':False}
            for box in box_seq:
                if loaded[box]===False:
                    while True:
                        look(img, )
                        pass        #do CV searching...



if name == "__main__":
	print("Auto Start")
	main()
	print("Mission Complete")

### Instruction:
# 1. Need RED CIRCLE on the car
# 2. Detect if car arrived
# 3. Arrived
# 4. Rotate to box side       <-control motors (90deg)
# 5. Search for box           <-control motors (x-axis)
# Loop*4     <-check the rules <-control motors (air, motor 90deg->90deg)
#     6. grab
#     7. throw
# 8. Return to init position  <-control motors (x-axis, 90deg)
# 9. time.sleep(10000)     <-10secs
# 
### Motor Side
# Listen to the port
# Do operation
# Feed Back when operation done