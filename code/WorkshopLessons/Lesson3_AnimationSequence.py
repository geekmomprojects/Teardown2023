# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Lesson 3 shows how to use the AnimationSequence class to control transitions
# between different animations
import neopixel
import board
import os
# For more info about Adafruit LED animations, see guide at https://learn.adafruit.com/circuitpython-led-animations
# or API documentation at https://docs.circuitpython.org/projects/led-animation/en/latest/
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.sequence import AnimationSequence

# Update to match the pin connected to your NeoPixels
# Make sure the pin is free
pixel_pin = eval("board." + os.getenv('LED_DATA_PIN'))
# Update to match the number of NeoPixels you have connected
pixel_num = 20
# Create the pixel array
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# Create several animation objects
blink = Blink(pixels, speed = 0.5, color=(255,128,0))
comet = Comet(pixels, speed=0.05, color=(0,255,0), tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=(0,128,128))

##### TODO: Create an AnimationSequence object to display animations in sequence