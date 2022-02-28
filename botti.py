# Imports
import time
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  # Mode, til ad nota pinoutid sem vid erum ad nota
GPIO.setwarnings(False)

# Fyrir hitanema
import board
#from adafruit_onewire.bus import OneWireBus

# Constants
STEP_SIZE= 1.8 # 1.8 Degrees but in microstepping
MAX_SOUP_TEMP = 40

# Variables
soup_type = "Aspas"

# Motor klassi
class Motor:
  def __init__(self, ID, pos, dir_pin, step_pin, dir, speed):
    self.ID = ID
    self.pos = pos
    self.dir_pin = dir_pin
    self.step_pin = step_pin
    self.dir = dir
    GPIO.setup(self.dir_pin, GPIO.OUT)
    GPIO.setup(self.step_pin, GPIO.OUT)
    self.speed = speed

  # Step, tekur motor og direction sem input, motor = 1 eda motor = 2, dir = 1 (rettsaelis) eda dir = 2 (rangsaelis)
  def step(self):
    GPIO.output(self.dir_pin, self.dir)
    GPIO.output(self.step_pin, 1)
    sleep(1/1000)
    GPIO.output(self.step_pin, 0)

  # Motor to degree
  def to_deg(self, deg):
    # Finna mismun
    diff = deg-self.pos
    if diff < 0:
      self.dir = False
      diff = -diff
    else:
      self.dir = True

    # Finna fjolda steps
    N_steps = int(diff/STEP_SIZE)*4

    # Steppa ad mismun
    for i in range(N_steps):
      self.step()
      sleep(1/self.speed)

# Setup
  # Motor 1
pos1 = 0
DIR1_PIN = 5
STEP1_PIN = 12
dir1 = True
speed1 = 10
mot1 = Motor(1, pos1, DIR1_PIN, STEP1_PIN, dir1, speed1)
  # Motor 2
pos2 = 0
DIR2_PIN = 6
STEP2_PIN = 13
dir2 = True
speed2 = 100
mot2 = Motor(2, pos2, DIR2_PIN, STEP2_PIN, dir2, speed2)
# Motors
motors = [mot1, mot2]
  # TempSensor
soup_temp = 100
#ow_bus = OneWireBus(board.D0)
#TEMP_PIN = 'P7'
#temp_sensor = DS18X20(OneWire())


# scan devices function
#def scan_devices():
#  devices = ow_bus.scan()
#  for d in devices:
#    print("ROM={}\tFamily=0x{:02x}".format(d.rom, d.family_code))

#def read_temp():
#  temper = temp.read_temp_async()
#  sleep(1)
#  temp.start_conversion()
#  sleep(1)
#  return temper


# Fara i nullstodu

# MAIN
#####################################################################3

# Snua einn hring
try:
  # Maela hita 
  #scan_devices()

  # Nidur ad supu
  motors[1].to_deg(36)
  motors[0].to_deg(18)

  # Greina supu
  print("Súpa: " + soup_type)

  '''
  # Maela supu
  while (soup_temp > MAX_SOUP_TEMP):
    # Blaka
    motors[1].to_deg(-9)
    motors[1].to_deg(9)
    # Maela
    soup_temp = read_temp()
  '''    

  # Prenta
  print("Soup temp: " + str(soup_temp))
  
  sleep(2)
  motors[1].to_deg(-36)
  sleep(1)
  motors[0].to_deg(-18)
  sleep(1)

except KeyboardInterrupt:
  GPIO.cleanup()
