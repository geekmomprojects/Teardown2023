import neopixel
import board
import time
# For more info about Adafruit LED animations, see https://learn.adafruit.com/circuitpython-led-animations
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from drop import Drop
from adafruit_led_animation.sequence import AnimationSequence

import os
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT


# Update to match the pin connected to your NeoPixels
# Make sure the pin is free
pixel_pin = eval("board." + os.getenv('LED_DATA_PIN'))
# Update to match the number of NeoPixels you have connected
pixel_num = 20
# Create the pixel array
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# Create the animation
pulse = Pulse(pixels, speed = 0.1, color=(255,128,0))
comet = Comet(pixels, speed=0.05, color=(0,255,0), tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=(0,128,128))

# Create the animation sequence
animations = AnimationSequence(
    comet, pulse, chase, advance_interval=5, auto_clear=True, random_order=True
)

mqtt_broker="mqtt.cheerlights.com"
mqtt_topic = "cheerlights"

### Code ###


# Define callback methods which are called when events occur
# TBD - Credit this code to Adafruit MQTT demo
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to Cheerlights!")


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from broker!")

def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(mqtt_topic, granted_qos))
    
def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(mqtt_topic, pid))

# TBD credit this code to author
def name_to_color(color):
   colors = {"red":(255,0,0),
             "green":(0,255,0),
             "blue":(0,0,255),
             "cyan":(0,255,255),
             "white":(255,255,255),
             "oldlace":(253,245,230),
             "purple":(128,0,128),
             "magenta":(255,0,255),
             "yellow":(255,255,0),
             "orange":(255, 165, 0),
             "pink":(255, 192, 203)
             }
   if color in colors:
       animations.color = colors[color]
       return colors[color]

    
def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    name_to_color(message)
    print("New message on topic {0}: {1}".format(mqtt_topic, message))

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=mqtt_broker,
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_subscribe = subscribe
mqtt_client.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()

print("Subscribing to %s" % mqtt_topic)
mqtt_client.subscribe(mqtt_topic)

#print("Disconnecting from %s" % mqtt_client.broker)
#mqtt_client.disconnect()

while True:
    # Poll the message queue
    mqtt_client.loop()
    animations.animate()
