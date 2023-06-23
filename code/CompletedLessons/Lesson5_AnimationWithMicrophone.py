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
        npix = self.pixel_object.n
        self.pixel_object.fill((0,0,0))
        height = clamp(int(self.mic.get_volume()*self.scale_vol), 0, npix)//2  #might need to scale mic values
        self.pixel_object[0:height] = [self.color]*height
        self.pixel_object[npix-height:npix] = [self.color]*height
        
     #TBD - introduce rolling averages, adjustable gain...
        
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
    
    # Mic pin attached here
    mic_pin = eval("board." + os.getenv('MIC_ADC_PIN'))
    mic = AnalogMIC(mic_pin, noise=13, nsamples = 120)
    
    vu_meter = VU_meter(pixels, mic, speed=0.01)
    while True:
        mic.record_sample()
        vu_meter.animate()