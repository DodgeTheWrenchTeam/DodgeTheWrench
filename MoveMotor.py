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

    def moveMotor(self, dir, speed, dist):
        assert ((dir == 'left') or (dir == 'right')), "\nUsage: moveMotor(dir, speed, dist)"
        if dir == "left":
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            GPIO.output(self.dirPin, GPIO.HIGH)

        distanceToSteps = int((dist / 60.0) * self.microstep)
        for step in range(distanceToSteps):
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(1 / (2 * (speed / 60.0) * self.microstep))
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(1 / (2 * (speed / 60.0) * self.microstep))

    def accelerate(self, dir, accelDist, decelDist, maxSpeed, dist):
        '''
        This function uses the 'time' and the maxSpeed to create a linear
        acceleration profile at the beginning and end of the motor movement.
        Inputs:
            dir         direction to move the motor [left, right]
            accelDist   distance at beginning of movement where the motor will accelerate
            decelDist   distance at end of movement where the motor will decelerate
            maxSpeed    the maximum speed the motor will move the cart, in mm/s 
            dist        the distance the motor will move the cart in total, in mm
        Outputs:
            None        Returns nothing, but sends pulse commands to motor driver
        '''
        assert ((dir == 'left') or (dir == 'right')), "\nUsage: accelerate(dir, time, maxSpeed, dist)"
        if dir == "left":
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            GPIO.output(self.dirPin, GPIO.HIGH)
            
        if accelDist <= 1:
            accelDist = 1
        if decelDist <= 1:
            decelDist = 1
        
        assert accelDist + decelDist <= dist, "accelStartDist + decelEndDist must be <= dist"

        distanceToSteps = int((dist / 60.0) * self.microstep)
        assert accelDist != 0 and decelDist != 0
        accelSteps = int((accelDist / 60.0) * self.microstep)
        decelSteps = int((decelDist / 60.0) * self.microstep)
        assert accelSteps >= 1 and decelSteps >= 1, "Acceleration/Deceleration distance is not large enough"

        minSpeed = 10 # change this if you want a higher starting/ending speed before the acceleration ramping
        
        accelSpeedChange = (maxSpeed - minSpeed) / accelSteps
        decelSpeedChange = (maxSpeed - minSpeed) / decelSteps

        speed = minSpeed - accelSpeedChange

        for step in range(distanceToSteps):
            if step < accelSteps:
                speed = speed + accelSpeedChange
            elif step >= distanceToSteps - decelSteps:
                speed = speed - decelSpeedChange
            if speed <= 0:
                continue
            if speed >= 1:
                GPIO.output(self.pulsePin, GPIO.HIGH)
                time.sleep(1 / (2 * (speed / 60.0) * self.microstep))
                GPIO.output(self.pulsePin, GPIO.LOW)
                time.sleep(1/ (2 * (speed / 60.0) * self.microstep))
            else:
                GPIO.output(self.pulsePin, GPIO.HIGH)
                time.sleep(1 / (2 * (minSpeed / 60.0) * self.microstep))
                GPIO.output(self.pulsePin, GPIO.LOW)
                time.sleep(1/ (2 * (minSpeed / 60.0) * self.microstep))


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
    #m.moveMotor("left", 1500, 300)
    #m.moveMotor("right", 1000, 300)
    #m.moveMotor("left", 500, 300)
    m.accelerate("right",.1,100,1000,300)
    m.accelerate("left",50,50,500,600)
    m.accelerate("right",100,100,1000,300)
    
