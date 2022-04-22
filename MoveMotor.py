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

        # Define the microstepping, 400 seems to work well.
        self.microstep = 200

    def moveMotor(self, dir, speed, dist):
        assert ((dir == 'left') or (dir == 'right')), "\nUsage: moveMotor(dir, speed, dist)"
        if dir == "left":
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            GPIO.output(self.dirPin, GPIO.HIGH)

        distanceToSteps = int((dist / 60.0) * self.microstep)
        sleep_time = 1 / (2 * (speed / 60.0) * self.microstep)
        for step in range(distanceToSteps):
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(sleep_time)
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(sleep_time)

    def accelerate(self, dir, accelDist, decelDist, maxSpeed, dist):
        '''
        This function uses the distances and the maxSpeed to create a linear
        acceleration profile at the beginning and end of the motor movement.
        Inputs:
            dir         direction to move the motor [left, right]
            accelDist   distance at beginning of movement where the motor will accelerate in mm
            decelDist   distance at end of movement where the motor will decelerate in mm
            maxSpeed    the maximum speed the motor will move the cart, in mm/s 
            dist        the distance the motor will move the cart in total, in mm
        Outputs:
            None        Returns nothing, but sends pulse commands to motor driver
        '''
        # Make sure direction is either 'left' or 'right'
        assert ((dir == 'left') or (dir == 'right')), "\nDistance must be 'left' or 'right'."
        if dir == 'left':
            GPIO.output(self.dirPin, GPIO.LOW)
        else:
            GPIO.output(self.dirPin, GPIO.HIGH)
        
        assert accelDist + decelDist <= dist, "\naccelStartDist + decelEndDist must be <= dist"

        distanceToSteps = int((dist / 60.0) * self.microstep) # Convert total distance to steps
        accelSteps = int((accelDist / 60.0) * self.microstep) # Convert acceleration distance to steps over which to accelerate
        decelSteps = int((decelDist / 60.0) * self.microstep) # Convert deceleration distance to steps over which to decelerate

        assert maxSpeed > 0, f"The maxSpeed must be greater than 0"

        # Catch case if accelSteps or decelSteps is 0
        if accelSteps == 0:
            accelSpeedChange = maxSpeed
        else:
            accelSpeedChange = maxSpeed / accelSteps
        if decelSteps == 0:
            decelSpeedChange = maxSpeed
        else:
            decelSpeedChange = maxSpeed  / decelSteps

        speed = 0

        for step in range(distanceToSteps):
            if step <= accelSteps:
                speed = speed + accelSpeedChange
            elif step > distanceToSteps - decelSteps:
                speed = speed - decelSpeedChange
            sleep_time = 1 / (2 * (speed / 60.0) * self.microstep)
            GPIO.output(self.pulsePin, GPIO.HIGH)
            time.sleep(sleep_time)
            GPIO.output(self.pulsePin, GPIO.LOW)
            time.sleep(sleep_time)


    def home(self, speed=100):
        # Initialize the endstop switch by first reading it's state.
        pressed = GPIO.input(self.homePin)
        while not pressed: # while switch has not been triggered (is still low from pulldown resistor)
            self.moveMotor("right", speed, 1) # Move 1mm towards endstop
            pressed = GPIO.input(self.homePin) # Check endstop switch
        time.sleep(0.5)
        # Go to middle of rail
        self.moveMotor('left', 300.0, 405.0)

if __name__ == "__main__":
    m = MoveMotor()
    m.home()
    #m.moveMotor("left", 1500, 300)
    #m.moveMotor("right", 1000, 300)
    #m.moveMotor("left", 500, 300)
    m.accelerate("right",50,100,1000,300)
    time.sleep(0.5)
    m.accelerate("left",50,50,500,600)
    time.sleep(0.5)
    m.accelerate("right",100,100,1000,300)
    time.sleep(0.5)
    accelerations = 60
    speed = 3000
    m.accelerate("left", accelerations, accelerations, speed, 300)
    time.sleep(0.25)
    for i in range(10):
        m.accelerate("right", accelerations, accelerations, speed, 300)
        time.sleep(0.25)
        m.accelerate("left", accelerations, accelerations, speed, 300)
        time.sleep(0.25)
    m.accelerate("right", accelerations, accelerations, speed, 600)
    time.sleep(0.25)
    for i in range(10):
        m.accelerate("left", accelerations, accelerations, speed, 300)
        time.sleep(0.25)
        m.accelerate("right", accelerations, accelerations, speed, 300)
        time.sleep(0.25)
    m.accelerate("left", accelerations, accelerations, speed, 300)
    
