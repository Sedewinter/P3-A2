# Imports go at the top
from microbit import *
import radio


# Code in a 'while True:' loop repeats forever
while True:
    radio.config(group=23)
    radio.on()
    radio.send('hello')
    message = radio.receive()
    if message:
       display.scroll(message)
    radio.off()
    