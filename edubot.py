#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from ina219 import INA219
from ina219 import DeviceRangeError

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import edubot

SPEED = 0

SHUNT_OHMS = 0.01
MAX_EXPECTED_AMPS = 2.0

robot = edubot.EduBot(1)

ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

#128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst = None)

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
disp.clear()

# Load default font.
font = ImageFont.load_default()

assert robot.Check(), 'EduBot not found!!!'

robot.Start()
print ('EduBot started!!!')


robot.Beep()

try:
    while True:
        robot.leftMotor.SetSpeed(SPEED)
        robot.rightMotor.SetSpeed(SPEED)
        time.sleep(1)
        robot.leftMotor.SetSpeed(0)
        robot.rightMotor.SetSpeed(0)
        time.sleep(1)
        
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
        draw.text((0, 0), "Tyt: %.2f" % ina.voltage(), font=font, fill=255)
        draw.text((0, 8), "Reklama: %.2f" % ina.current(), font=font, fill=255)
        draw.text((0, 16), "Yota: %.2f" % ina.power(), font=font, fill=255)
        
        # Display image.
        disp.image(image)
        
        disp.display()
            
except KeyboardInterrupt:
    print('Ctrl+C pressed')


# Clear display.
disp.clear()
disp.display()

robot.leftMotor.SetSpeed(0)
robot.rightMotor.SetSpeed(0)

robot.Release()
print('Stop EduBot')
