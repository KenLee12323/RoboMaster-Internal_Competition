### This program helps user to pick color range with HSV color bar ###
### Red, Blue, Green, Yellow, Dark -> svae as json file           ###
### KenLee1223 10/28/2019                                         ###

import cv2
import numpy as np
from getkey import getkey, keys

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

cam = cv2.VideoCapture(0)

def nothing(x):
    pass
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

data = {}
while True:
    _, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    cv2.waitKey(33)
    key = getkey(blocking=False).decode('utf-8') #convert bytes to str

    # Find color range for Red
    if key == 'r' or key == 'R':
        data['lower_red'] = lower_range
        data['upper_red'] = upper_range
    # Find color range for Blue
    elif key == 'b' or key == 'B':
        data['lower_blue'] = lower_range
        data['upper_blue'] = upper_range
    # Find color range for Green
    elif key == 'g' or key == 'G':
        data['lower_green'] = lower_range
        data['upper_green'] = upper_range
    # Find color range for Yellow
    elif key == 'y' or key == 'Y':
        data['lower_yellow'] = lower_range
        data['upper_yellow'] = upper_range
    # Find color range for Black
    elif key == 'd' or key == 'D':
        data['lower_black'] = lower_range
        data['upper_black'] = upper_range
    elif key =='q' or key =='Q':    
        data_str = json.dumps(data, cls=NumpyEncoder)
        with open('colors_ranges.json', 'w') as fp:
            json.dump(data_str, fp)
        break

cam.release()
cv2.destroyAllWindows()


# # load back json file
# with open('colors_ranges.json', 'r') as fp:
#     data = json.load(fp)
# data = json.loads(data,cls=NumpyDecoder)



