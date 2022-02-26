"""
This file contains the functions to move the stepper motor. 
Function inputs:
dir       direction of movement: "left" or "right"
speed     integer 1-10 for relative speed of motor
dist      distance to move in mm 
"""


class MoveMotor:
    def __init__(self):
        # Define pins for motor pulse, direction, and homing switch
        self.pulsePin = 24
        self.dirPin = 23
        self.homePin = 25
        # Initialize GPIO pins
        GPIO.setup(self.pulsePin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.dirPin, GPIO.OUT, initial=GPIO.LOW)
        #GPIO.setup(EN, GPIO.OUT) # sets EN as an output pin
        # Sets  homePin as an input with a pull-down resistor
        GPIO.setup(self.homePin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def moveMotor(self,dir,speed,dist):

