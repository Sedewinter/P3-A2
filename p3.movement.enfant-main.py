from microbit import *
import radio

radio.on()
key = "Key" 

def movement():
    while True:
        
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        movement_intensite = x**2 + y**2 + z**2
        if movement_intensite < 20000:
            state="Endormei"
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
