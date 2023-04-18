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
close_claw_speed = -200
open_claw_speed = 200
raise_arm_speed = -200
lower_arm_speed = 200
clockwise_turning_speed = 200

pick_up = -170
first_drop_off = -460
second_drop_off = -610
third_drop_off = -720
read_color_height = -480

ev3.speaker.beep()

def ResetClawAngle():
   # Set closed claw angle to 0 when closed
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.reset_angle(0)

def ResetArmAngle():
   # Set highest position as 0 degrees
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   arm_motor.reset_angle(0)

def ResetTurningAngle():
   turning_motor.run_until_stalled(clockwise_turning_speed, then=Stop.HOLD, duty_limit=50)
   turning_motor.reset_angle(0)

def ResetRobot():
   ResetClawAngle()
   ResetArmAngle()
   ResetTurningAngle()
   turning_motor.run_target(-200, pick_up, then=Stop.HOLD)
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)
   claw_motor.run_target(open_claw_speed, 90, then=Stop.HOLD)

def PickUpItem():
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=100)
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=50)
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)

def DropItem():
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.run_target(open_claw_speed, 90, then=Stop.HOLD)
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)

def IsObjectInLocation(drop_off_zone):
   ResetRobot()
   
   # Turn to given angle
   turning_motor.run_target(clockwise_turning_speed, drop_off_zone, then=Stop.HOLD)

   # Try to pick up item
   PickUpItem()

   claw_angle = claw_motor.angle()

   if claw_angle > 0:
      print("There is an object in the location")
      DropItem()
      
   else:
      print("No object in location")
   
def ReadColorAndDropInLocation():
   ResetRobot()
   wait(1000)

   PickUpItem()
   wait(1000)

   # read color
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)
   print(color_sensor.color())
   
   DropItem()

def DropOffDependentOnColor():
   ResetRobot()

   PickUpItem()

   item_color = color_sensor.color()
   print(item_color)
   
   if item_color == Color.RED:
      turning_motor.run_target(-200, first_drop_off, then=Stop.HOLD)
   elif item_color == Color.GREEN:
      turning_motor.run_target(-200, second_drop_off, then=Stop.HOLD)
   elif item_color == Color.YELLOW:
      turning_motor.run_target(-200, third_drop_off, then=Stop.HOLD)
   elif item_color == Color.BLUE:
      turning_motor.run_target(-200, third_drop_off, then=Stop.HOLD)
   
   DropItem()




# old functions
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
   arm_motor.run_target(50, 460, then=Stop.HOLD)
   wait(5000)
   print(color_sensor.color())

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




#IsObjectInLocation(second_drop_off)