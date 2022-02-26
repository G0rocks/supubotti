# Imports
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  # Mode, til ad nota pinoutid sem vid erum ad nota


# Setup
DIR_PIN = 5
STEP_PIN = 12

GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)


# Fara i nullstodu

step_size = 1.8 # Degrees

# Step, tekur att i input, dir = 1 (rettsaelis) eda dir = 2 (rangsaelis)
def step(dir):
  GPIO.output(DIR_PIN, dir)
  GPIO.output(STEP_PIN, 1)
  GPIO.output(STEP_PIN, 0)


# Snua einn hring
try:
  N = 200
  direction = 1

  for i in range(4*N):
    step(direction)

except KeyboardInterrupt:
  GPIO.cleanup()
