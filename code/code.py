# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Any file named "code.py" will run by default at CircuitPython startup
# More information on the CircuitPython led_animation class can be found at
# https://learn.adafruit.com/circuitpython-led-animations
# or API documentation at https://docs.circuitpython.org/projects/led-animation/en/latest/
import neopixel
import board
import time
import os

# Import Animations
from fall import Fall
from drop import Drop
from mic import AnalogMIC
from vu_meter import VU_meter
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence

# Update to match the pin connected to your NeoPixels
pixel_pin = eval("board." + os.getenv('LED_DATA_PIN'))
# Update to match the number of NeoPixels you have connected
pixel_num = 20
# Create the pixel array
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# Uncomment the animations you'd like to add to the sequence
animation_list = []
#animation_list.append(Fall(pixels, speed=0.05, color=(0,255,0)))
animation_list.append(Drop(pixels, speed=0.05, color=(0,255,255)))
#animation_list.append(RainbowChase(pixels, speed=0.1, size=5, spacing=3))
animation_list.append(RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True))
#animation_list.append(RainbowSparkle(pixels, speed=0.1, num_sparkles=15))
#animation_list.append(RainbowTwinkle(pixels, speed = 0.02))

# If using the microphone, uncomment lines below as well as
# the call to mic.record_sample() in the main loop
#mic_pin = board.IO4
#mic = AnalogMIC(mic_pin, nsamples = 30)
#animation_list.append(VU_meter(pixels, mic, speed = 0.05))

# Create the animation sequence
animations = AnimationSequence(*animation_list,
                               advance_interval = 30,
                               auto_clear = True)


max_volume = 0
while True:
#    mic.record_sample()  #If using microphone, uncomment this line
    animations.animate()

