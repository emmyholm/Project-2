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


# Write your program here.
ev3.speaker.beep()
#turning_motor.run_angle(100, -90, then=Stop.HOLD)


#open_claw = 50


# claw_motor.reset_angle(0)
# wait(5000)


#claw_motor.run_target(50, 45 ,then=Stop.HOLD)
# wait(5000)


def ResetClawAngle():
   close_claw_speed = -100


   # Set closed claw angle to 0 when at lowest position
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.reset_angle(0)


def PickUpAndPutDown():


   close_claw_speed = -100
   open_claw_speed = 50
   raise_arm_speed = -100
   lower_arm_speed = 100


   ResetClawAngle()


   # Open claw 90 degrees
   claw_motor.run_target(open_claw_speed, 90 ,then=Stop.HOLD)
   wait(5000)


   # Pick up item (close claw)
   claw_motor.run_until_stalled(close_claw_speed, then=Stop.HOLD, duty_limit=100)
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)


   # Put down
   arm_motor.run_until_stalled(lower_arm_speed, then=Stop.HOLD, duty_limit=50)
   claw_motor.run_target(open_claw_speed, 90 ,then=Stop.HOLD)
   arm_motor.run_until_stalled(raise_arm_speed, then=Stop.HOLD, duty_limit=50)




#while True:5
 # print(color_sensor()) # Hitta färger som finns runtomkring
  #print(turning_motor.angle()) # Vilken vinkel som den befinner sig på
  #wait(500)




# while True:
 # print(color_sensor.rgb()) # Kollar också vilken färg sensioren uppfattar men mer trovärdigt ger lite mer exakta värden
 # wait(500)

