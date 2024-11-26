from microbit import *
import radio
from math import *

radio.on()
radio.config(group=99)
key = "BROOKS" 

def movement():
    while True:
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        z_movement = abs(z - 1024)
        movement_intensite = x**2 + y**2 + z**2
        grimpage_intensite = sqrt(x) + sqrt(y) + z**3
        if z_movement>500000:
            state=detection_grimpage()
        if movement_intensite < 20000:
            state="Endormi"
        elif 20000 <= movement_intensite < 100000:
            state="Agité"
        else:  
            state="Trés_agité"
        radio.send(state)
        if state=="Endormi":
            display.show(Image.SMILE)
        elif state=="Agité":
            display.show(Image.SAD)
        elif state=="Trés_agité":
            display.show(Image.ANGRY)
        sleep(1000)    
movement()

def detection_grimpage():
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    z_movement = abs(z - 1024)
    climbing_duration=0
    while z_movement>500000:
        climbing_duration+=1
        if climbing_duration>10:
            state="CLIMBING"
            return state