# Imports
from time import sleep

from sympy import true
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  # Mode, til ad nota pinoutid sem vid erum ad nota

# Constants
STEP_SIZE= 1.8 # 1.8 Degrees but in microstepping

# Motor klassi
class Motor:
  def __init__(self, ID, pos, dir_pin, step_pin, dir):
    self.ID = ID
    self.pos = pos
    self.dir_pin = dir_pin
    self.step_pin = step_pin
    self.dir = dir
    GPIO.setup(self.dir_pin, GPIO.OUT)
    GPIO.setup(self.step_pin, GPIO.OUT)

  # Step, tekur motor og direction sem input, motor = 1 eda motor = 2, dir = 1 (rettsaelis) eda dir = 2 (rangsaelis)
  def step(self):
    GPIO.output(self.dir_pin, self.dir)
    GPIO.output(self.step_pin, 1)
    sleep(1/400)
    GPIO.output(self.step_pin, 0)

  # Motor to degree
  def to_deg(self, deg):
    # Finna mismun
    diff = deg-self.pos
    if diff < 0:
      self.dir = False
    else:
      self.dir = True

    # Finna fjolda steps
    N_steps = int(diff/STEP_SIZE)*4

    # Steppa ad mismun
    for i in range(N_steps):
      self.step()



# Setup
  # Motor 1
pos1 = 0
DIR1_PIN = 5
STEP1_PIN = 12
dir1 = True
mot1 = Motor(1, pos1, DIR1_PIN, STEP1_PIN, dir1)
  # Motor 2
pos2 = 0
DIR2_PIN = 6
STEP2_PIN = 13
dir2 = True
mot2 = Motor(2, pos2, DIR2_PIN, STEP2_PIN, dir2)
# Motors
motors = [mot1, mot2]
  # TempSensor




# Fara i nullstodu

# MAIN
#####################################################################3

# Snua einn hring
try:
  #motors[0].to_deg(18)
  motors[1].to_deg(18)

except KeyboardInterrupt:
  GPIO.cleanup()
