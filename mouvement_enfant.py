from microbit import *
import radio
import music

radio.on()
key = "Key" 

biberon = Image("19991:""09090:""92229:""09290:""09290")

def berceuse():
    music.play(music.PRELUDE)

def alarme():
    music.play(music.PYTHON)
    

def milk_quantity(milk):
    for _ in range(5):
        display.show(milk)
        sleep(200)
        display.show(biberon)
        sleep(1000)
        sleep

def movement():
    last_state = None
    while True:
        message = radio.receive()
        if pin_logo.is_touched():
            return False
        if message == "berceuse":
            berceuse()
        elif message == "alarme":
            alarme()
            
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        movement_intensite = (x**2 + y**2 + z**2)*0.5
        if movement_intensite < 1000000:
            state="Endormi"
        elif 1000000 <= movement_intensite < 2000000:
            state="Agité"
        else:  
            state="Trés_agité"
        
        if state=="Endormi":
            display.show(Image.SMILE)
        elif state=="Agité":
            display.show(Image.SAD)
        elif state=="Trés_agité":
            display.show(Image.ANGRY)

        if last_state != state:
            radio.send(state)
        last_state = state
        sleep(100)

display.show(Image.HEART_SMALL)
sleep(700)
        
milk = 0
while True:
    message = radio.receive()
    try:
        milk = int(message)
    except TypeError:
        pass
    
    if pin_logo.is_touched():
        milk_quantity(milk)            
    else:
        movement()
