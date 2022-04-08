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
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

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
            print("WARNING: Direction not specified!")

        distanceToSteps = int((dist / 60.0) * self.microstep)
        for step in range(distanceToSteps):
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(1 / (2 * (speed / 60.0) * self.microstep))
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(1 / (2 * (speed / 60.0) * self.microstep))

    def home(self):
        # Check endstop switch
        pressed = GPIO.input(self.homePin)
        while not pressed: # while switch has not been triggered (is still low from pulldown resistor)
            self.moveMotor("right", 100, 1) # Move 1mm towards endstop
            pressed = GPIO.input(self.homePin)
        time.sleep(0.5)
        # Go to middle of rail
        self.moveMotor('left', 300.0, 405.0)

if __name__ == "__main__":
    m = MoveMotor()
    m.home()
    m.moveMotor("left", 1500, 300)
    m.moveMotor("right", 1000, 300)
    m.moveMotor("left", 500, 300)
