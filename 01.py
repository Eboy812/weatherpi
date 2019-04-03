#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import sys
import time




from PIL import ImageFont

import smbus2
import bme280

def do_nothing(obj):
    pass

# define our i2c LED location
serial = i2c(port=1, address=0x3C)
# We have an ssd1306 device so we initialize it at the
# serial address we created.
device = ssd1306(serial)
# This line keeps the display from immediately turning off once the
# script is complete.
device.cleanup = do_nothing

# Setup our Temperature sensor (bme280)
port = 4
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

def lan_ip():
    cmd = 'hostname -I'
    f = os.popen(cmd)
    ip = str(f.read())
    return "IP Address: %s" % ip.rstrip('\r\n').rstrip('')

def main():
    data = bme280.sample(bus, address, calibration_params)
    freesans = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Black.ttf',20)
    freesans15 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Black.ttf',15)
    freesans12 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Black.ttf',12)
    freesans10 = ImageFont.truetype('/usr/share/fonts/truetype/lato/Lato-Black.ttf',10)
    Piboto15 = ImageFont.truetype("Piboto-Regular.ttf", 15)
    
    with canvas(device) as draw:
        #draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5,10), "%3.2f\u00b0F" % (data.temperature*9/5+32), font=freesans15, fill="white")
        draw.text((0,0), "Room Temp:", font=freesans12, fill="white")
        draw.text((1,37), str(data.timestamp), font=freesans15, fill="white")
        draw.text((25,23), "Time-Date:", font=freesans15, fill="white")
        draw.text((75,0), "Humidity:", font=freesans12, fill="white")
        draw.text((75,10), "%3.2f" % (data.humidity), font=freesans15, fill="white")
        draw.text((115,10), "%", font=freesans15, fill="white")
        #draw.text((46,10), "F", font=freesans15, fill="white")
        draw.text((8,52), (lan_ip()), font=freesans10, fill="white")
        
        print (data.temperature*9/5+32)
while True:
    main()
    time.sleep(10)
    
    
