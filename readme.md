1. CV_Optional_Task: Folder for the CV optional task.
                     The algorithm find the balls' trajectory by getting the frame residue.
                     The frame residue is filtered by sobel filter and then ordinary Hough transform. 
                     This method is very good when the camera is steady, given the assumption
                     that all objects are moving very slowly relative to the ball.
                     The computation requirement is low as well given that the frame is resized.
                     
                     A better method that can be done by referencing from epipo-line in finding correspondances.
                     First, the ball trajectory is found.
                     Second, look for the shooting machine along the line of the trajectroy with ordinary CV techni.
                     Third, applying optical flow to check for the movement of the shooting machine to estimate 
                     the coming ball trajectory.
                     However, the computation requirement is high when there is no GPU.
                     
2. Laptop_Mining_Machine: Folder for the Laptop part of the minig machine.
                          bullshit.py: The running program for the first game rules' version.
                          bullshit2.py: The running program for the lastest game rules' version.
                                        It is connected with UART to listen to the command
                                        and usb to control the mining machine
                                        and the given camera to do the CV task.
                                        
                                        The CV task first tramsform the frame from RBG to HSV color space.
                                        A better color space would be Lab CIE.
                                        However, it would require a bit more computation resources.
                                        Second, the code will control the mining machine to move horizontally
                                        to look for the required box.
                                        A threshold is set to check if a certain box exist.
                                        If yes, refine the location and grab.
                                        If not, keep searching.
                          matchBox.py: Simple code to help user create a json file storing the range of
                                       each box's HSV color space.
                          colors_ranges.json: A json file storing the range of each box's HSV color space.
                          port.py: Testing the UART port communication and mining machine communication.
                          Other files: Helper codes for function testing.
3. Mining_Machine: Folder for mining machine control.
                   main.c: The code for controling machine movement,
                           including signal receiving from laptop, motor control and sending backing signal to laptop for successful action.
                   Other files: for motor, PID and device control.
                   (This part is yet to be finished and the progress is suspended since last Firday give the current situation.
                   Codes aer not tested.)
                   
                          
