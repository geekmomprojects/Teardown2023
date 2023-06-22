# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Lesson 4 demonstrates creating a new animation class that inherits from the
# led_animation Animation class to take advantage of its timing and display
# functionality

from adafruit_led_animation.animation import Animation  #This is the base class
from adafruit_led_animation.color import RAINBOW, calculate_intensity       #RAINBOW: List of color tuples in the rainbow
                                                                            #calculate_intensity() scales down the brightness of a color
import time
import random
import math

BLACK = (0,0,0)
# Create a new animation that inherits from the Animation base class. This RandomPixel
# animation causes pixels along the LED strip to light up randomly, then fade away
class RandomPixel(Animation): 
    
    # A new animation class must contain two functions. (1) an __init__ function that
    # calls the __init__ function of its superclass and (2) a draw() function that
    # modifies the pixels to create the patterns for each animation frame
    def __init__(
        self,
        pixel_object,
        speed=0.05,     # Frame rate
        prob=0.005,     # Probability of pixel lighting up with each call
        color=(255,0,0),
        name=None
        ):
        # Initialize the base class
        super().__init__(pixel_object, speed, color=color, name=name)
        self.prob = prob 
        self.reset()
    
    def reset(self):
        self.pixel_object.fill(BLACK)
    
    # Define this simple function so we can override it in a child class
    def _pixel_color(self): 
        return self.color
        
    # Override the draw function to create the
    def draw(self):
        for i, pixel in enumerate(self.pixel_object):
            if pixel == BLACK:
                if random.random() < self.prob:  # Pixel will flip if random value in [0,1] < prob
                    # We set the pixel color using a member function so that we can change
                    # the way the colors are chosen in a child class
                    self.pixel_object[i] = self._pixel_color()
            else:
                pixel = calculate_intensity(pixel, 0.95)         # Slightly dim each illuminated pixel
                if (pixel[0] + pixel[1] + pixel[2])/3 < 15:      # Below a certain threhold turn it off
                    pixel = BLACK
                self.pixel_object[i] = pixel
                
class RandomRainbowPixel(RandomPixel):
    def __init__(
        self,
        pixel_object,
        speed=0.05,   #Frame rate
        prob=0.005,   #Probability of pixel lighting up with each call
        color=(255,0,0),
        name=None
        ):
        # Initialize the base class
        super().__init__(pixel_object, speed=speed, prob = prob, color=color, name=name)
        
    def _pixel_color(self):
        return random.choice(RAINBOW)
    
                
            
# For testing the class
if __name__ == "__main__":
    import neopixel
    import board
    import os
    
    # Update to match the pin connected to your NeoPixels
    # Make sure the pin is free
    pixel_pin = eval("board." + os.getenv('LED_DATA_PIN'))
    # Update to match the number of NeoPixels you have connected
    pixel_num = 20
    # Create the pixel array
    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)
    
    # Create the animation object - either RandomPixel or RandomRainbowPixel
    rp = RandomPixel(pixels, prob=0.01, speed=0.03, color=(0,255,255))
    
    # Call animate() to handle animation timing
    while True:
        rp.animate()
            
                      