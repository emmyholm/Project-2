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
touch_sensor = TouchSensor(Port.S1)

close_claw_speed = -200
open_claw_speed = 200
raise_arm_speed = -200
lower_arm_speed = 200
clockwise_turning_speed = 200

holding_object_claw_angle = 10

pick_up = - 70
read_color_height = -410

first_drop_off = pick_up - 310
second_drop_off = first_drop_off - 150
third_drop_off = second_drop_off - 130

ev3.speaker.beep()

# Set default angles
def ResetRobot():
   # Reset arm angle
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   arm_motor.reset_angle(0)
   # Set arm height to color reading height
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)

   # Reset claw angle and set to open claw
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.reset_angle(0)
   # Set claw to open
   claw_motor.run_target(open_claw_speed, 90, then=Stop.HOLD)
   
   # Reset turning angle
   turning_motor.run_until_stalled(clockwise_turning_speed, then=Stop.HOLD, duty_limit=50)
   turning_motor.reset_angle(0)
   # Set turning angle to pick up
   turning_motor.run_target(-200, pick_up, then=Stop.HOLD)

def PickUpItem():
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=20)
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=50)
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)

def DropItem():
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.run_target(open_claw_speed, 90, then=Stop.HOLD)
   arm_motor.run_target(raise_arm_speed, read_color_height, then=Stop.HOLD)

# Test for configuring drop off locations
def TestDropOff():
   ResetRobot()

   turning_motor.run_target(-200, first_drop_off, then=Stop.HOLD)
   PickUpItem()
   turning_motor.run_target(-200, second_drop_off, then=Stop.HOLD)
   PickUpItem()
   turning_motor.run_target(-200, third_drop_off, then=Stop.HOLD)
   PickUpItem()

def DropItemAtLocation(drop_off_zone):
   ResetRobot()

   ev3.speaker.say('I will pick up the item')

   PickUpItem()

   claw_angle = claw_motor.angle()
   
   if claw_angle > holding_object_claw_angle:
      ev3.speaker.say('Turning and dropping in given location')
      turning_motor.run_target(-200, drop_off_zone, then=Stop.HOLD)
      DropItem()
   else:
      ev3.speaker.say('No item found')

def IsObjectInLocation(drop_off_zone):
   ResetRobot()

   ev3.speaker.say('Checking for object in given location')
   
   # Turn to given angle
   turning_motor.run_target(clockwise_turning_speed, drop_off_zone, then=Stop.HOLD)

   # Try to pick up item
   PickUpItem()

   claw_angle = claw_motor.angle()

   if claw_angle > holding_object_claw_angle:
      # Check color
      item_color = color_sensor.color()
      
      # Message
      ev3.speaker.say('There is a' + str(item_color).replace('Color.', '') + ' object in the location')
      
      DropItem()
      
   else:
      ev3.speaker.say("I can't find an object in the given location, sorry")

def SortItems(seconds_delay_start, seconds_delay_between_attempts, total_attempts):
   ResetRobot()
   claw_angle = 0
   no_item_found_count = 0

   if seconds_delay_start > 0:
      ev3.speaker.say('Starting pick up process in ' + str(seconds_delay_start) + 'seconds')
      wait(seconds_delay_start * 1000)

   while no_item_found_count < total_attempts:
      
      # Try to pick up item
      ev3.speaker.say('Trying to pick up item')
      PickUpItem()
      claw_angle = claw_motor.angle()

      # No object found, wait and try again if attempts left
      if claw_angle < holding_object_claw_angle:
         no_item_found_count = no_item_found_count + 1

         # Speaker message
         speaker_message = 'No item found, ' + str(total_attempts - no_item_found_count) + 'attempts left '
         if seconds_delay_between_attempts > 0 and no_item_found_count < total_attempts:
            speaker_message = speaker_message + 'I will try again in ' + str(seconds_delay_between_attempts) + 'seconds'

         ev3.speaker.say(speaker_message)

         # Delay time
         wait(seconds_delay_between_attempts * 1000)

         # Open claw again
         claw_motor.run_target(open_claw_speed, 90, then=Stop.HOLD)

      # Item found
      else:
         item_color = color_sensor.color()
         ev3.speaker.say(str(color_sensor.color()).replace('Color.', ''))
         
         # Turn dependent on color
         if item_color == Color.RED:
            turning_motor.run_target(-200, first_drop_off, then=Stop.HOLD)

         elif item_color == Color.GREEN:
            turning_motor.run_target(-200, second_drop_off, then=Stop.HOLD)

         elif item_color == Color.YELLOW:
            turning_motor.run_target(-200, third_drop_off, then=Stop.HOLD)

         elif item_color == Color.BLUE:
            turning_motor.run_target(-200, third_drop_off, then=Stop.HOLD)

         else:
            ev3.speaker.say('Unknown Color')
         
         DropItem()

         # Return to pick up location
         turning_motor.run_target(-200, pick_up, then=Stop.HOLD)


# Drop at given location
# US02b
#DropItemAtLocation(second_drop_off)

# Checking color and if object is in location
# US01b, US03, US04b
#IsObjectInLocation(pick_up)

# Sorting and drop off
# US05, US08b, US09, US10
#SortItems(5, 2, 2)
