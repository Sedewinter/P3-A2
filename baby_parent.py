from microbit import *
import radio
import music

radio.on()
radio.config(group=99,power=5)
biberon = Image("19991:""09090:""92229:""09290:""09290")
should_exit=0

def set_radion_frequency_band(band: int):
    return band

def check_frequency():
    band=0 
    if set_radion_frequency_band(band)>50:
        music.play(music.BA_DING)#remplacer par alarme
        sleep(200)
        
check_frequency()

def milk_quantity(milk):
    max_milk=10
    min_milk=0
    for _ in range(5):
        if button_a.is_pressed() and button_b.is_pressed():
            milk = 0
            display.show(milk)
            sleep(1000)
            display.clear()
        if button_a.get_presses():
            if milk>min_milk:
                milk-=1
                display.show(milk)
                sleep(500)
        if button_b.get_presses():
            if milk<max_milk:
                milk+=1
                display.show(milk)
                sleep(500)
            else:
                display.show("TOO MUCH MILK!")
                audio.play(Sound.SOARING, wait=False)
        sleep(100)
        display.show(milk)
        sleep(500)
        display.show(biberon)
        sleep(1000)
        sleep
    return milk
        

def alerting():
        
    last_message = ""
    
    while True:
        message = radio.receive()
        if pin_logo.is_touched():
            return False

        if button_a.get_presses():
            radio.send("berceuse")

        elif button_b.get_presses():
            radio.send("alarme")
            
        if message == "Agité" and last_message != "Agité":
            display.show(Image.SMILE)
            audio.play(Sound.GIGGLE, wait=False)
            last_message = "Agité"
            
        elif message == "Trés_agité":
            display.show(Image.CONFUSED)
            audio.play(Sound.SOARING, wait=False)
            last_message = "Trés_agité"
            
        elif message == "Endormi":
            display.show("Z")
            last_message = "Endormi"
            
        elif message == "climbing":
            for _ in range(10):
                music.play(music.BA_DING, wait=False)
                display.show(Image.GIRAFFE)
                sleep(1000)
            last_message = "climbing"


display.show(Image.HEART)
sleep(800)

milk = 0
while True:
    if pin_logo.is_touched():
        milk = milk_quantity(milk)            
    else:
        alerting()
        
