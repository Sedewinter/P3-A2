from microbit import *
import music
def set_radion_frequency_band(band: int):
    return band
    
def check_frequency():
    band=0
    if set_radion_frequency_band(band)>50:
        music.play(music.BA_DING)#remplacer
        sleep(200)
check_frequency()
            
    
    
def milk_quantity():
    biberon = Image("19991:"
                 "09090:"
                 "92229:"
                 "09290:"
                 "09290")
    sleep(500)
    milk=0
    max_milk=10
    min_milk=0
    #sean_add_milk()#TBD
    while True:
        display.show(biberon)
        if button_b.get_presses():
            if milk<max_milk:
                milk+=1
                display.show(milk)
                sleep(300)
        if button_a.get_presses():
            if milk>min_milk:
                milk-=1
                display.show(milk)
                sleep(300)
        if button_a.is_pressed() and button_b.is_pressed():
                milk=0
                display.show(milk)
                sleep(1000)
        display.show(biberon)
        sleep(1000)
        display.show(milk)
        sleep(1000)


touch_count=0
while True:
    if pin_logo.is_touched():
        touch_count+=1
        if touch_count%2==1:
            milk_quantity()
        else:
            display.show(Image.DUCK) #call function for accelerometer