import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('balls.avi')
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Get frame width and height
#     print(gray.shape[:2])

ret0, frame0 = cap.read()
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Display the resulting frame
    # cv2.imshow('Frame',frame)

    ### Gray->MdeianBlur->Bilinear-Int Reszie 1/3 (1024, 1280)
    # Img(t-1)
    gray0 = cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)
    blurred0 = cv2.medianBlur(gray0, 3, 0)
    resized0 = cv2.resize(blurred0, (160,128))
    # Img(t)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 3, 0)
    resized = cv2.resize(blurred, (160,128))

    # Img Difference (Assume objects station /slow motion)
    resized = resized.astype("int16")
    resized0 = resized0.astype("int16")
    frame1 = np.absolute(resized - resized0)
    frame1 = frame1.astype("uint8")

    # Non-maximum Suppression (replace with thresholding)
    # frame1[frame1<15] = 0
    # cv2.imshow('Frame',frame1)
    
    # Hough transform
    edges = cv2.Canny(frame1,150,230, apertureSize = 3)
    # cv2.imshow('edges', edges)
    
    lines = cv2.HoughLines(edges,1,np.pi/180,22) # Or try HoughLinesP
    if lines is not None:
        temp = [0,0,0,0]
        for rho,theta in lines[:,0,:]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            temp[0] += (x0 + 1000*(-b))
            temp[1] += (y0 + 1000*(a))
            temp[2] += (x0 - 1000*(-b))
            temp[3] += (y0 - 1000*(a))
        no_lines = len(lines[:,0,:])
        x1 = int((temp[0]/no_lines)*8)
        y1 = int((temp[1]/no_lines)*8)+10 			# adjustment (shift)
        x2 = int((temp[2]/no_lines)*8)
        y2 = int((temp[3]/no_lines)*8)+10 			# adjustment (shift)
        gray = cv2.line(gray,(x1,y1),(x2,y2),(0,0,255), 3)
    cv2.imshow('HoughFrame',gray)

    # Store current frame as last frame
    ret0, frame0 = ret, frame

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break


 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()