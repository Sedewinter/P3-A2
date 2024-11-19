from microbit import *
import radio
#We need to stock milk quantity (in dl), display it, and reset it on a button press.
#Nice bonus include displaying the quantity in different colors in function of the quantity, having a milk smiley, etc.


def milk_quantity():
    biberon = Image("19991:"
                 "09090:"
                 "92229:"
                 "09290:"
                 "09290")
    sleep(500)
    milk=7
    #sean_add_milk()#TBD
    for i in range(50):
        if button_a.get_presses()>=2 and button_b.get_presses()>=2:
            milk=0
            display.show(milk)
            sleep(1000)
            display.show(Image(""))
            break
        display.show(milk)
        sleep(5000)
        display.show(biberon)
        sleep(1000)
milk_quantity()


#We need to do "a sudden 'jumping' detector".
#Basically we want to detect instances when a baby is climbing - or trying to climb- a safety barrier.
#The baby could also try to climb on the kitchen - which would be very dangerous.



value=500
value=500
def climb_detector():
    alarm=False
    if accelerometer.get_z() > value and accelerometer.get_x() > 5 : # We need to determine a value of height. The x thing is just to check this is not a false positive.
         #Logically,in any climbing, you slightly move forward.
         alarm=True
         return alarm
def alarm():
    radio.on()
    radio.send('CLIMBING')
def climb_alarm():
    for i in range(1,10):
        set_volume(255)
        music.play(music.BA_DING, wait=False)
        display.show(Image.GIRAFFE)
        sleep(1000)
