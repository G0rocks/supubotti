print("Starting")
# Imports
import time
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  # Mode, til ad nota pinoutid sem vid erum ad nota
GPIO.setwarnings(False)

# Fyrir hitanema
import os
import glob
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Constants
STEP_SIZE= 1.8 # 1.8 Degrees but in microstepping
MAX_SOUP_TEMP = 25

# Variables
#soup_type = "Aspas"

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

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Fara i nullstodu

# MAIN
#####################################################################3

# Snua einn hring
try:
  while(True):
    print("Na i supu")
    # Nidur ad supu
    motors[1].to_deg(36)
    motors[0].to_deg(27)

    # Greina supu
    #print("S??pa: " + soup_type)

    # Maela supu
    print("Maelir supu")
    #sleep(10)
    #print(". ")
    #sleep(10)
    #print(". ", end = "")
    #sleep(10)
    #print(". ", end = "")
    temp1 = read_temp()
    sleep(3)
    soup_temp = read_temp()
    temp_diff = soup_temp - temp1
    while(temp_diff > 0):
      temp1 = read_temp()
      sleep(3)
      soup_temp = read_temp()
      temp_diff = soup_temp - temp1
      print("Hitastig: " + str(soup_temp) + "??C")

    motors[1].speed = 20
    while (soup_temp > MAX_SOUP_TEMP):
      print("Supa of heit")
      # Blaka
      motors[1].to_deg(-9)
      sleep(1)
      motors[1].to_deg(9)
      # Maela
      soup_temp = read_temp()
      # Prenta
      print("Hitastig: " + str(soup_temp) + "??C")
    motors[1].speed = speed2
    print("Supa passlega heit")

    sleep(2)
    motors[1].to_deg(-27)
    sleep(1)
    motors[0].to_deg(-27)
    sleep(8)
    motors[1].to_deg(-9)

except KeyboardInterrupt:
  GPIO.cleanup()

print("Done")
