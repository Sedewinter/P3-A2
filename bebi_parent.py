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
    if set_radion_frequency_band(band)>15:
        music.play(music.BA_DING)#remplacer par alarme
        sleep(200)
        
# def check_frequency():
#     # Check if the radio group is set correctly
#     band = radio.config()['group']
#     if band != 99:
#         music.play(music.BA_DING)  # Play an alert if the group is incorrect
#         sleep(200)
def milk_quantity(milk):
    max_milk=10
    min_milk=0
    for _ in range(5):
        check_frequency()
        if button_a.is_pressed() and button_b.is_pressed():
            milk = 0
            radio.send("0")
            display.show(milk)
            sleep(1000)
            display.clear()
        if button_a.get_presses():
            if milk>min_milk:
                milk-=1
                radio.send(str(milk))
                display.show(milk)
                sleep(500)
        if button_b.get_presses():
            if milk<max_milk:
                milk+=1
                radio.send(str(milk))
                display.show(milk)
                sleep(500)
            else:
                display.show("MAX!")
                music.play(music.WAWAWAWAA, wait=False)
        sleep(100)
        display.show(milk)
        sleep(1000)
        display.show(biberon)
        sleep(1000)
    return milk



def receive():
  while True:
      packet = radio.receive()
      if packet:
          if packet=="Endormi":
              display.show(Image.SMILE)
          elif packet=="Agité":
              display.show(Image.SAD)
          elif packet=="Trés_agité":
              display.show(Image.ANGRY)
          else:
              display.scroll("UNKNOWN")

      sleep(1000)

def alerting():
        
    last_message = ""
    
    while True:
        check_frequency()
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

        elif message == "chaud":
            display.show(Image("90909:""09990:""99999:""09990:""90909"))
            for _ in range(5):
                music.play(["C6:2", "C6:2", "G5:2", "G5:2"])
            sleep(100)

        elif message == "froid":
            display.show(Image("90909:""09090:""90909:""09090:""90909"))
            for _ in range(5):
                music.play(["C6:2", "C6:2", "G5:2", "G5:2"])
            sleep(100)


display.show(Image.HEART)
sleep(800)

milk = 0


while True:
    if pin_logo.is_touched():
        milk = milk_quantity(milk)            
    else:
        alerting()