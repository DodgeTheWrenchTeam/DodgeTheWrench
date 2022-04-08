#!/usr/bin/env python3

import cv2
import depthai as dai
import cvzone
from cvzone.ColorModule import ColorFinder
import math
from Avoidance import DodgeWrench
from MoveMotor import MoveMotor
import time
from time import sleep
import imutils
from collections import deque
import argparse
# Initialize MoveMotor, home linear actuator
move = MoveMotor()
##move.home()

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")

# Properties
windowHeight = 300
windowWidth = 300
camRgb.setPreviewSize(windowWidth, windowHeight)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Linking
camRgb.preview.link(xoutRgb.input)
pts = []
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 26, 'smin': 22, 'vmin': 168, 'hmax': 56, 'smax': 227, 'vmax': 255}
# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    print('Connected cameras: ', device.getConnectedCameras())
    # Print out usb speed
    print('Usb speed: ', device.getUsbSpeed().name)

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    positionlist = []
    
    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
        img = inRgb.getCvFrame()
        
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(img, width=300)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        #imgColor, mask = myColorFinder.update(img,hsvVals)
        
        #imgContour, contours = cvzone.findContours(img,mask,minArea=50)
        #(x,y), radius = cv2.minEnclosingCircle(contours)
        #center = (int(x),int(y))
        #radius = int(radius)
        #circ = cv2.circle(img,center,radius,(0,255,0),2)
        
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        #only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 1:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                # update the points queue
                x = int(x - 150)
                y = int(150 - y)
                d = 31
                z = int(d / (2 * math.tan(radius/2)) + 100)
                positionlist.append([x,y,z])
                #pts.append(positionList)
                if len(positionlist) > 10:
                    print(positionlist)
                    position1 = positionlist[0]
                    position2 = positionlist[10]
                    #print(positionlist)
                    positionlist.pop(0)
                    print("position 1,2: " + str(position1) + "," + str(position2))
                
                    # Run avoidance script to determine direction and distance for avoidance
                    dirMove, dirDist = DodgeWrench(position1, position2, 400)
                    print("Direction: " + str(dirMove) + "\nDistance: " + str(dirDist))

                    # Move motor the appropriate direction, then move back to center.
                    if (dirMove == "right"):
                        print("Avoidance is a go!" + "\nDirection: " + str(dirMove))
                        #superRunTime = time.time() - begin
                        #print('Command Time =', superRunTime)
                        move.moveMotor("right",2000,200)
                        #superRunTime = time.time() - begin
                        #print('Net Time =', superRunTime)
                        time.sleep(1)
                        move.moveMotor("left",1000,200)
                        time.sleep(1)
                        positionlist = []

                    elif (dirMove == "left"):
                        print("Avoidance is a go!" + "\nDirection: " + str(dirMove))
                        #superRunTime = time.time() - begin
                        #print('Command Time =', superRunTime)
                        move.moveMotor("left",2000,200)
                        #superRunTime = time.time() - begin
                        #print('Net Time =', superRunTime)
                        time.sleep(1)
                        move.moveMotor("right",1000,200)
                        time.sleep(1)
                        positionlist = []
                        
                    else:
                        print("do not avoid")
            #print(pts)
            #imgStack = cvzone.stackImages([img,imgColor,mask,imgContour],2,.5)
            """
        if contours:
            x = contours[0]['center'][0] - windowWidth / 2
            y = windowHeight - contours[0]['center'][1] - windowHeight/2
            area = int(contours[0]['area'])
            # Note: this Z position is really not correct, it's just a rough estimate
            radius = math.sqrt(area/math.pi)
            z = round(100 - radius,3)
            # Compensating for pixels to real numbers
            x = (31.5/math.sqrt(area/math.pi))*x
            y = (31.5/math.sqrt(area/math.pi))*y
            data = x,y,z
            print(data)
            positionlist.append([x,y,z])

            if len(positionlist) > 5:
                position1 = positionlist[0]
                position2 = positionlist[5]
                #print(positionlist)
                positionlist.pop(0)
                print("position 1,2: " + str(position1) + "," + str(position2))
            
                # Run avoidance script to determine direction and distance for avoidance
                dirMove, dirDist = DodgeWrench(position1, position2, 400)
                print("Direction: " + str(dirMove) + "\nDistance: " + str(dirDist))

                # Move motor the appropriate direction, then move back to center.
                if (dirMove == "right"):
                    print("Avoidance is a go!" + "\nDirection: " + str(dirMove))
                    #superRunTime = time.time() - begin
                    #print('Command Time =', superRunTime)
                    move.moveMotor("right",2000,200)
                    #superRunTime = time.time() - begin
                    #print('Net Time =', superRunTime)
                    time.sleep(1)
                    move.moveMotor("left",1000,200)
                    time.sleep(1)

                elif (dirMove == "left"):
                    print("Avoidance is a go!" + "\nDirection: " + str(dirMove))
                    #superRunTime = time.time() - begin
                    #print('Command Time =', superRunTime)
                    move.moveMotor("left",2000,200)
                    #superRunTime = time.time() - begin
                    #print('Net Time =', superRunTime)
                    time.sleep(1)
                    move.moveMotor("right",1000,200)
                    time.sleep(1)
                    
                else:
                    print("do not avoid")
                """
        # Retrieve 'bgr' (opencv format) frame
        cv2.imshow("rgb", frame)

        
        
        if cv2.waitKey(1) == ord('q'):
            break

