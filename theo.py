from microbit import *
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
