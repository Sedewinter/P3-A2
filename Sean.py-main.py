from microbit import *
touch_count=0
while True:
    if pin_logo.is_touched():
        touch_count+=1
        if touch_count%2==1:
            display.show(Image.HEART)
        else:
            display.show(Image.DUCK)