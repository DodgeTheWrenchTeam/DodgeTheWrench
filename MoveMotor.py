"""
This file contains the functions to move the stepper motor. 
Function inputs:
dir       direction of movement: "left" or "right"
speed     speed in mm/s
dist      distance to move in mm 
"""

import RPi.GPIO as GPIO
import time

class MoveMotor:
    def __init__(self):
        # Define pins for motor pulse, direction, and homing switch
        self.dirPin = 23
        self.pulsePin = 24
        self.homePin = 25
        
        # Initialize GPIO pins
        GPIO.setup(self.pulsePin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.dirPin, GPIO.OUT, initial=GPIO.LOW)
        # Sets homePin as an input with a pull-down resistor
        GPIO.setup(self.homePin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        # Define the microstepping
        self.microstep = 400

    def moveMotor(self,dir,speed,dist):
        if dir == "left":
            GPIO.output(self.dirPin, GPIO.LOW)
        elif dir == "right":
            GPIO.output(self.dirPin, GPIO.HIGH)
        else:
            print("Usgae: moveMotor(dir, speed, dist)")
            print("Please enter a valid direction ('left' or 'right')")
            # Do we want to import sys and use sys.exit(1) here to exit the program?
            print("Using 'right' as default")
            GPIO.output(self.dirPin, GPIO.HIGH)

        distanceToSteps = (dist / 60.0) * self.microstep
        for step in range(distanceToSteps):
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(1 / (2 * (speed / 60.0) * self.microstep))
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(1 / (2 * (speed / 60.0) * self.microstep))

    def home(self):
        GPIO.output(self.dirPin, GPIO.HIGH)
        pressed = GPIO.input(self.homePin)
        while not pressed: # while switch has not been triggered (is still low from pulldown resistor)
            # provide one pulse to the motor to turn it one step
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(0.002)
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(0.002)
            pressed = GPIO.input(self.homePin)

        #Move off of homing switch a constant amount, no matter the microstep amout
        time.sleep(0.5)
        GPIO.output(self.dirPin, GPIO.LOW)
        for step in range(int(self.microstep/6)): # 1/6 of a revolution = 10mm off from switch
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(0.002)
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(0.002)
        time.sleep(0.5)
