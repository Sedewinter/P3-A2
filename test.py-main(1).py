# Imports go at the top
from microbit import *
import radio
        display.scroll("baby"+ "mario")
        radio.on()
        while True:
            message = radio.receive()
            if message:
               display.scroll(message.upper.strip""")
display.scroll("B=",b)