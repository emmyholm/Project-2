#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                               InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
turning_motor = Motor(Port.C)
arm_motor = Motor(Port.B)
claw_motor = Motor(Port.A)
color_sensor = ColorSensor(Port.S2)
close_claw_speed = -100
open_claw_speed = 50
raise_arm_speed = -100
lower_arm_speed = 100
turning_speed = 100

ev3.speaker.beep()

def ResetClawAngle():
   # Set closed claw angle to 0 when closed
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.reset_angle(0)

def ResetArmAngle():
   # Set highest position as 0 degrees
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)
   arm_motor.reset_angle(0)
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)

def PickUpAndPutDown():
   ResetClawAngle()
   ResetArmAngle()

   # Open claw and insert item
   claw_motor.run_target(open_claw_speed, 90 ,then=Stop.HOLD)
   wait(5000)

   # Pick up item
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=100)
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)

   # Put down
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.run_target(open_claw_speed, 90 ,then=Stop.HOLD)
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)

def IsObjectInLocation(angle):
   ResetClawAngle()
   ResetArmAngle()
   
   # Reset turning motor
   turning_motor.reset_angle(0)

   # Raise arm and open claw
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.run_target(open_claw_speed, 90 ,then=Stop.HOLD)
   
   # Turn to given angle
   turning_motor.run_target(turning_speed, angle, then=Stop.STOP)

   # Try to pick up item
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   wait(5000)
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=100)

   claw_angle = claw_motor.angle()

   if claw_angle > 0:
      print("There is an object in the location")
   else:
      print("No object in location")

def PickUpAndReadColor():
   ResetClawAngle()
   ResetArmAngle()

   # Lower arm and open claw to insert item
   claw_motor.run_target(50, 90 ,then=Stop.HOLD)
   wait(5000)
   
   # Pick up item
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=100)
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)

   # Lower arm to color sensor and check color
   arm_motor.run_target(50, 425, then=Stop.HOLD)
   wait(5000)
   print(color_sensor.color())

#US01, US02
#PickUpAndPutDown()

#US03
#ObjectInLocation(0)

#US04
#PickUpAndReadColor()