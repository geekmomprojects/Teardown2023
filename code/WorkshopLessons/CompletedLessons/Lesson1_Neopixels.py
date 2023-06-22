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

# Colors are  represented as RGB tuples
BLACK = (0,0,0)
RED = (255,0,0)

#Change pixel colors in the while loop. Don't forget to call "show()"
while True:
    n = pixel_num//2
    pixels[0::2] = [RED]*n      # Use a python slice to color alternate pixels red (R,G,B)
    pixels[1::2] = [BLACK]*n    # This slice colors the remaining pixels black
    pixels.show()               # Must call show() to see changes
    time.sleep(0.2)
    
    pixels[0::2] = [BLACK]*n    # Reverse the pattern
    pixels[1::2] = [RED]*n
    pixels.show()
    time.sleep(0.2)
    