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

# Create the animation. Speed parameter is time between animation frames
comet = Comet(pixels, speed=0.05, color=(0,255,0), tail_length=6, bounce=True)
chase = Chase(pixels, speed=0.1, color=(255,0,0), size = 3, spacing = 2, reverse=False)

# Call animate to generate animations. LED animations library takes care of timing
while True:

    # Calling animate() on the animation object updates and displays
    # the animation, taking care of the timing without blocking so that
    # other functionality can be called in the main code loop
    
    # uncomment one of the animations below to see it
    #chase.animate() 
    comet.animate()