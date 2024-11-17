from microbit import *

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


touch_count=0
while True:
    if pin_logo.is_touched():
        touch_count+=1
        if touch_count%2==1:
            milk_quantity()
        else:
            display.show(Image.DUCK) #call function for accelerometer