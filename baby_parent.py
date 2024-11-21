from microbit import *
import radio
import music
radio.on()
radio.config(group=99)

biberon = Image("19991:""09090:""92229:""09290:""09290")

def set_radion_frequency_band(band: int):
    return band
    
def check_frequency():
    band=0 
    if set_radion_frequency_band(band)>50:
        music.play(music.BA_DING)#remplacer par alarme
        sleep(200)
check_frequency()           
def milk_quantity():
    milk = 0
    max_milk=10
    min_milk=0
    while True:
        if pin_logo.is_touched():
            display.clear()
            return False
        if button_a.is_pressed() and button_b.is_pressed():
            milk = 0
            display.show(milk)
            sleep(1000)
            display.clear()
            return True
        if button_a.get_presses():
            if milk>min_milk:
                milk-=1
                display.show(milk)
                sleep(300)
        if button_b.get_presses():
            if milk<max_milk:
                milk+=1
                display.show(milk)
                sleep(300)
            else:
                display.show("TOO MUCH MILK!")
                audio.play(Sound.SOARING, wait=False)
        

        display.show(milk)
        sleep(200)
        display.show(biberon)
        sleep(1000)
    return False

def alerting():

    last_message = ""
    
    while True:
        message = radio.receive()
        
        if pin_logo.is_touched():
            display.clear()
            return False
        
        if message == "agite" and last_message != "agite":
            display.show(Image.SMILE)
            audio.play(Sound.GIGGLE, wait=False)
            last_message = "agite"
            
        elif message == "alerte":
            display.show(Image.CONFUSED)
            audio.play(Sound.SOARING, wait=False)
            last_message = "alerte"
            
        elif message == "endormi":
            display.show("Z")
            last_message = "endormi"
            
        elif message == "CLIMBING":
            for i in range(10):
                music.play(music.BA_DING, wait=False)
                display.show(Image.GIRAFFE)
                sleep(1000)
            last_message = "CLIMBING"
        sleep(100)


display.show(Image.HEART)
sleep(3000)
display.clear()

milk_mode = False

# while True:
#     if milk_mode:
#         milk_mode = milk_quantity() 
#     else:
#         milk_mode = not alerting()


while True:
    if pin_logo.is_touched():
        milk_quantity()
    else:
        alerting()