from adafruit_led_animation.animation import Animation
from mic import AnalogMIC

def clamp(x, minv, maxv):
    return max(minv, min(x, maxv))

class VU_meter(Animation):
    
    def __init__(
        self,
        pixel_object,
        mic_object,
        speed=0.05,
        color=(255,0,0),
        name=None
    ):
         super().__init__(pixel_object, speed, color, name=name)
         self.mic = mic_object
         
    def draw(self):
        npix = self.pixel_object.n
        self.pixel_object.fill((0,0,0))
        height = clamp(int(self.mic.get_volume()), 0, npix-1)//2
        self.pixel_object[0:height] = [self.color]*height
        self.pixel_object[npix-height:npix] = [self.color]*height
        
     #TBD - introduce rolling averages, adjustable gain...
        
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
    
    # Mic pin attached here
    mic_pin = board.IO4
    mic = AnalogMIC(mic_pin, nsamples = 30)
    
    vu_meter = VU_meter(pixels, mic, speed=0.01)
    while True:
        mic.record_sample()
        vu_meter.animate()