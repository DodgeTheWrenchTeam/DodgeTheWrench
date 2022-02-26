import RPi.GPIO as GPIO
import time # TODO: figure out a better way than sleeping

GPIO.setmode(GPIO.BCM)

PUL = 24
DIR = 23
SWITCH = 25

CW = 0
CCW = 1
MICROSTEPPING = 400
FREQ = 8000
DELAY = 1 / (2 * FREQ)

GPIO.setup(PUL, GPIO.OUT, initial=GPIO.LOW) # sets PUL as an output pin
GPIO.setup(DIR, GPIO.OUT, initial=GPIO.LOW) # sets DIR as an output pin
#GPIO.setup(EN, GPIO.OUT) # sets EN as an output pin
GPIO.setup(SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # sets SWITCH pin as an input with a pullup resistor (switch will pull signal down to ground)

#Homing Sequence
GPIO.output(DIR, CCW) # set direction to CCW for homing

pressed = GPIO.input(SWITCH)
while not pressed: # while switch has not been triggered (is still low from pulldown resistor)
    # provide one pulse to the motor to turn it one step
    GPIO.output(PUL, GPIO.HIGH) # set output as high
    time.sleep(0.002) # wait for motor to turn
    GPIO.output(PUL, GPIO.LOW) # set output as low
    time.sleep(0.002) # wait for motor to turn
    pressed = GPIO.input(SWITCH)
    print(pressed)
    
#Move off of homing switch
time.sleep(0.5)
GPIO.output(DIR, CW)
for step in range(int(MICROSTEPPING/8)):
    GPIO.output(PUL, GPIO.LOW) # set output as high
    time.sleep(0.002) # wait for motor to turn
    GPIO.output(PUL, GPIO.HIGH) # set output as low
    time.sleep(0.002) # wait for motor to turn
time.sleep(0.5)

# Go to middle of rail
GPIO.output(DIR, CW)
for step in range(int(MICROSTEPPING * 6.9)):
    GPIO.output(PUL, GPIO.LOW) # set output as high
    time.sleep(DELAY) # wait for motor to turn
    GPIO.output(PUL, GPIO.HIGH) # set output as low
    time.sleep(DELAY) # wait for motor to turn
time.sleep(1)

GPIO.output(DIR, CCW)
for step in range(int(MICROSTEPPING * 2)):
    GPIO.output(PUL, GPIO.LOW) # set output as high
    time.sleep(DELAY) # wait for motor to turn
    GPIO.output(PUL, GPIO.HIGH) # set output as low
    time.sleep(DELAY) # wait for motor to turn

GPIO.output(DIR, CW)
for step in range(int(MICROSTEPPING * 4)):
    GPIO.output(PUL, GPIO.LOW) # set output as high
    time.sleep(DELAY) # wait for motor to turn
    GPIO.output(PUL, GPIO.HIGH) # set output as low
    time.sleep(DELAY) # wait for motor to turn

GPIO.output(DIR, CCW)
for step in range(int(MICROSTEPPING * 2)):
    GPIO.output(PUL, GPIO.LOW) # set output as high
    time.sleep(DELAY) # wait for motor to turn
    GPIO.output(PUL, GPIO.HIGH) # set output as low
    time.sleep(DELAY) # wait for motor to turn

GPIO.cleanup() # releases pins for other uses
