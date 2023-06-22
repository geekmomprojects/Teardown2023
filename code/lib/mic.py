# Demo code.py for Teardown 2023 workshop: LED Animations with CircuitPython
# Class to record and average data from an analog microphone
import analogio
import board
import math
import array


# Helper functions
def mean(values):
    return sum(values) / len(values)

def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
    return math.sqrt(samples_sum / len(values))

def peak_to_peak(values):
    return max(values) - min(values)
    
# Analog microphone class
# mic_pin: 	ADC pin with microphone input
# noise: 	baseline noise to subract (will need to experiment with values)
# nsamples: number of readings to average
class AnalogMIC():
    def __init__(self, mic_pin, noise=13, nsamples=160):
        self.mic = analogio.AnalogIn(mic_pin)
        self.nsamples=nsamples
        self.samples = array.array('H',[0]*self.nsamples) 	# Circular buffer to store readings
        self.sample_index = 0								# Index to circular buffer
        self.noise = noise  # Baseline value to subract. Determined experimentally

    # Call this function in the main loop to collect sound samples
    def record_sample(self):
        v = int((self.mic.value/65536)*1000) 			#10-bit ADC format
        self.samples[self.sample_index] = abs(v - 512)  #Subract center
        self.sample_index = (self.sample_index + 1) % self.nsamples

    # Return the average sound level
    def get_volume(self):
        return max(mean(self.samples) - self.noise, 0)
