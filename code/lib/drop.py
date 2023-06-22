# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# This code inherits from the Adafruit led_animation.animation class to display
# a drop moving under constant acceleration one both sides of an LED string.

from adafruit_led_animation.animation import Animation 			# Animation the base class
from adafruit_led_animation.color import RAINBOW				# A list of colors in the rainbow
from adafruit_led_animation.color import calculate_intensity	# Function to scale color intensity
import time
import random
import math

# Acceleration & velocity values for motion under constant acceleration
# according to the formula for position: x = x0 + v0*t + 1/2*a*t*t
# Units of time are seconds, units of distance are pixels
# Change the values below to change the initial velocity and acceleration
# of the falling drops
ACC = 1.2  # pixels/sec^2
V0 = 1.6   # pixels/sec

# LED animation that has a single drop falling under "gravity" from the top (middle)
# of the lanyard to the end of the lanyard
class Drop(Animation): #Our class will inherit from the Animation class
    
    # We need to create an instructor and override the draw function
    def __init__(
        self, pixel_object, speed, color=(0,0,255), name=None
        ):
        # Call base class constructor to initialize it
        super().__init__(pixel_object, speed, color=color, name=name)
        # Initialize member variables
        # Always start in the middle of the string
        self.start_pos = (self.pixel_object.n-1)/2
        # Can accelerate either direction.
        # Acceleration and velocity must have same sign
        self.acc = random.choice([-1,1])*ACC
        self.vel = math.copysign(V0,self.acc) 
        self.drop_time = time.monotonic()
        
    # Create a function to get called once the drop finishes falling
    # We can use this to change the color of the drop in a class that
    # inherits from this one
    def _reset_drop(self):
        self.drop_time = time.monotonic()
        self.acc = random.choice([-1,1])*ACC
        self.vel = math.copysign(V0,self.acc)
        
    
    def draw(self):
        #Calculate drop position
        dt = time.monotonic() - self.drop_time
        dist = self.vel*dt + 0.5*self.acc*dt*dt  #d = v0*t + 1/2*a*t^2

        # Drop fell off the ends, reset but don't draw
        if abs(dist) > self.start_pos:
            self._reset_drop()
            return
        
        # Compute drop position
        pos = self.start_pos - dist
         
        # Erase old pixels
        self.pixel_object.fill((0,0,0))
        
        # If object is "between" pixels, split the light and intensity between both
        pos0 = int(math.ceil(pos))
        val = 1.0 - abs(pos-pos0) 		# intensity decreases with distance between pixel and drop position
        self.pixel_object[pos0] = calculate_intensity(self.color, val*val)
        
        pos1 = int(math.floor(pos))
        if pos1 != pos0:
            val = 1.0 - val                     #other pixel is exactly 1 unit away
            self.pixel_object[pos1] = calculate_intensity(self.color, val*val)
        
# This class has the exact same functionality as the Drop class, but the
# drop colors vary with colors of the rainbow. Override the _get_color()
# function to allow the drops to have different random colors
class RainbowDrop(Drop):
    # Init funciton calls the base class constructor
    def __init__(
        self, pixel_object, speed, color=(0,0,255), name=None
        ):
        # Call base class constructor to initialize it
        super().__init__(pixel_object, speed, color=color, name=name)
    
    # Override the _reset_drop() function to make the drops random colors
    def _reset_drop(self):
        self.color = random.choice(RAINBOW)
        super()._reset_drop()
        
        
    
# For testing
if __name__ == "__main__":
    import neopixel
    import board
    
    # Update to match the pin connected to your NeoPixels
    # Make sure the pin is free
    pixel_pin = board.SCL
    # Update to match the number of NeoPixels you have connected
    pixel_num = 20
    # Create the pixel array
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)
    
    # Uncomment the correct line for the animation you want
    #drop = Drop(pixels, speed=0.01)
    drop = RainbowDrop(pixels, speed=0.01)
    
    while True:
        drop.animate()
