# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Lesson 5 creates an animation that responds to input from the microphone by
# displaying VU meter-like light columns on both sides of the lanyard. This 
# animation uses a microphone class found in /lib/mic.py for collecting data
# from an analog microphone and averaging it over time. 

from adafruit_led_animation.animation import Animation # Base class for the animation we'll create
from mic import AnalogMIC                              # Class to read and average input from MAX4466 microphone

# Helper function
def clamp(x, minv, maxv):
    return max(minv, min(x, maxv))

# The VU_meter animation fills the pixels symmetrically in columns on both sides of the
# lanyard string. The height of the columns reflect the average measured noise
# intensity. The microphone must be attached to the microcontroller.
class VU_meter(Animation):
    def __init__(
        self,
        pixel_object,  # Pixel array
        mic_object,    # Microphone object to sample and average sound
        speed=0.05,    # Time between animation frames
        color=(255,0,0),
        name=None
    ):
         # Initialize the base class
         super().__init__(pixel_object, speed, color, name=name)
         self.mic = mic_object
         self.scale_vol = 1.0  # Adjusts the range of volume displayed
         
    # Override the led_animation class draw() function to display the vu_meter animation 
    def draw(self):
    ##### TODO: Fill in the draw function
        
    # future improvements - introduce rolling averages, adjustable gain...
        
# For testing
if __name__ == "__main__":
    import neopixel
    import board
    import time
    import os
    
    # Update to match the pin connected to your NeoPixels
    # Make sure the pin is free
    pixel_pin = eval("board." + os.getenv('LED_DATA_PIN'))
    # Update to match the number of NeoPixels you have connected
    pixel_num = 20
    # Create the pixel array
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)
 
    ##### TODO: Create a microphone object to read from the ADC pin receiving microphone input
    
    ##### TODO: Create a vu_meter animation object that takes the microphone object as an argument

    while True:
    ##### TODO: add functions to the main loop to sample microphone data and display the vu_meter animation
