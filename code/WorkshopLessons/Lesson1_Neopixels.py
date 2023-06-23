# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Lesson 1 shows how to use the pixel array to change pixel colors and
# to display those colors by calling the show() function
import neopixel
import board
import time
import os

# Update to match the pin connected to your NeoPixels
pixel_pin = eval("board." + os.getenv('LED_DATA_PIN'))
# Update to match the number of NeoPixels you have connected
pixel_num = 20
# Create the pixel array
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

###### TODO: Add code here to change and display the pixel colors