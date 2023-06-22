# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
from adafruit_led_animation.animation import Animation # Inherit functionality from Animation base class
import rainbowio
import time
import random

# This animation fills the sides of the lanyard with falling pixels in rainbow
# colors then resets when the sides are full
class Fall(Animation): 
    
    # We only need to create an instructor and override the draw function
    # The rest of the functionality (timing, display) come from the base class
    def __init__(
        self, pixel_object, speed, color=(255,0,0), name=None
        ):
        #Call base class constructor
        super().__init__(pixel_object, speed, color=color, name=name)
        half_pix = self.pixel_object.n//2
        self.last_pix = 0
        self.falling_pos = half_pix
        self.last_time = 0
        self.drop_interval = 0.1
        self.colors = [0]*(half_pix+1)
        #Create rainbow colors
        self.set_hues(0)
            
    def set_hues(self, base=None):
        half_pix = self.pixel_object.n//2
        if base is None:
            base = random.randint(0,255)
        for i in range(half_pix+1):
            self.colors[i] = (rainbowio.colorwheel((base + i*255/(half_pix+1))% 255))
        
        
    # Returns the index of the mirror pixel if the string is folded in the middle
    def pair(self, n):
        return self.pixel_object.n - 1 - n
        
    # Override the draw function to make our class do what it wants
    def draw(self):
        npix = self.pixel_object.n
        self.pixel_object.fill((0,0,0))
        # Draw fallen pixels
        for i in range(self.last_pix):
            self.pixel_object[i] = self.colors[i]
            self.pixel_object[self.pair(i)] = self.colors[i]
        # Draw falling pixels
        self.pixel_object[self.falling_pos] = self.colors[self.last_pix]
        self.pixel_object[self.pair(self.falling_pos)] = self.colors[self.last_pix]
        
        # See if it's time to move the falling pixel downwards
        if time.monotonic() - self.last_time > self.drop_interval:
            if self.last_pix == self.pixel_object.n//2:   # Columns have been filled
                self.last_pix = 0
                self.falling_pos == self.pixel_object.n//2
                self.set_hues()  # Reset color stack
            elif self.falling_pos == self.last_pix:       # Falling pixel has reached resting position
                self.last_pix = self.last_pix + 1
                self.falling_pos = self.pixel_object.n//2
            else:                                         # Pixel still falling
                self.falling_pos = self.falling_pos - 1
            
            self.last_time= time.monotonic()
            
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
    
    fall = Fall(pixels, speed=0.01)
    while True:
        fall.animate()
            
        