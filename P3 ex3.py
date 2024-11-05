from microbit import *
import radio




while True:
    radio.on()
    radio.config(group=7)
    if button_a.is_pressed():
        radio.send("happy")
    if button_b.is_pressed():
        radio.send("sad")
    message=radio.receive()
    if message=="sad":
        display.show(Image.SAD)
    if message=="happy":
        display.show(Image.HAPPY)
    radio.off()
    


    









