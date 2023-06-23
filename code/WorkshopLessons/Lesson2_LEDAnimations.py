# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Lesson 2 demonstrates how to create and display animations from the
# animation classes in the adafruit_led_animation library
import neopixel
import board
import os

# Import led animation modules
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase


# Update to match the pin connected to your NeoPixels
pixel_pin = board.eval("board." + os.getenv('LED_DATA_PIN'))
# Update to match the number of NeoPixels you have connected
pixel_num = 20
# Create the pixel array
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

##### TODO: Add code here to display animations from the Adafruit led_animation library