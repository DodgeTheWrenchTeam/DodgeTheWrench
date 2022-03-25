#!/usr/bin/env python3

import cv2
import depthai as dai
import cvzone
from cvzone.ColorModule import ColorFinder
import math
from Avoidance import DodgeWrench
from MoveMotor import MoveMotor
import time

# Initialize MoveMotor, home linear actuator
move = MoveMotor()
move.home()

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

# Linking
camRgb.preview.link(xoutRgb.input)

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
        imgColor, mask = myColorFinder.update(img,hsvVals)
        
        imgContour, contours = cvzone.findContours(img,mask,minArea=50)
        #imgStack = cvzone.stackImages([img,imgColor,mask,imgContour],2,.5)
        
        if contours:
            x = contours[0]['center'][0] - windowWidth / 2
            y = windowHeight - contours[0]['center'][1] - windowHeight/2
            area = int(contours[0]['area'])
            # Note: this Z position is really not correct, it's just a rough estimate
            radius = math.sqrt(area/math.pi)
            z = round(100 - radius,3)
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
                
        # Retrieve 'bgr' (opencv format) frame
        cv2.imshow("rgb", imgContour)

        
        
        if cv2.waitKey(1) == ord('q'):
            break
