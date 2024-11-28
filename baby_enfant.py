from microbit import *
import radio
import music

radio.on()
radio.config(group=99)
key = "Key" 

biberon = Image("19991:""09090:""92229:""09290:""09290")

musique_berceuse = [    
    "G4:4", "A4", "G4", "E4",
    "G4:4", "C5", "B4:8",
    "A4:4", "G4", "F4", "D4",
    "G4:4", "A4", "G4:8",
    "C5:4", "D5", "C5", "B4", 
    "G4:4", "A4", "G4:8" 
]

musique_alarme = [
    "C6:2", "G5:2", "C6:2", "G5:2",
    "F5:2", "A5:2", "F5:2", "A5:2",
    "C6:2", "G5:2", "C6:2", "G5:2",
    "E5:2", "C5:2", "E5:2", "C5:2"
]

def saut_mouton():
    mouton1 = Image("00000:""00000:""00000:""00000:""00807")
    mouton2 = Image("00000:""00000:""00000:""00070:""00800")
    mouton3 = Image("00000:""00000:""00700:""00000:""00800")
    mouton4 = Image("00000:""00000:""00000:""07000:""00800")
    mouton5 = Image("00000:""00000:""00000:""00000:""70800")
    mouton6 = Image("00000:""00000:""00000:""00000:""00800")
    frames = [mouton1, mouton2, mouton3, mouton4, mouton5, mouton6]
    for frame in frames:
        display.show(frame)
        sleep(700)

def signal():
    signal1 = Image("00000:""00000:""00000:""00000:""00000")
    signal2 = Image("00000:""00000:""00600:""00000:""00000")
    signal3 = Image("00000:""00700:""07770:""00700:""00000")
    signal4 = Image("00800:""08980:""89998:""08980:""00800")
    signal5 = Image("00000:""00700:""07770:""00700:""00000")
    signal6 = Image("00000:""00000:""00600:""00000:""00000")
    frames = [signal1, signal2, signal3, signal4, signal5, signal6]
    for frame in frames:
        display.show(frame)
        sleep(350)


def berceuse():
    for _ in range(3):
        music.play(musique_berceuse, wait=False)
        saut_mouton()
        saut_mouton()
    return None

def alarme():
    for _ in range(5):
        music.play(musique_alarme, wait=False)
        signal()
        signal()
    return None   

def milk_quantity(milk):
    for _ in range(5):
        display.show(milk)
        sleep(1000)
        display.show(biberon)
        sleep(1000)
        sleep

def movement():
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    last_state = None
    while True:
        message = radio.receive()
        tem=temperature()
        if pin_logo.is_touched():
            break
            
        if message == "berceuse":
            message = berceuse()
        elif message == "alarme":
            message = alarme()
        elif message in numbers:
            return int(message)

        if tem>25:
            radio.send("chaud")
        elif tem<17:
            radio.send("froid")
            
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
            display.show(Image.SILLY)
        elif state=="Trés_agité":
            music.play(musique_berceuse, wait=False)
            display.show(Image("99999:""99999:""99999:""99999:""99999"))
            sleep(4000)

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
        if message is not None:
            milk = int(message)
    except TypeError:
        pass
    
    if pin_logo.is_touched():
        milk_quantity(milk)            
    else:
        is_it_milk = movement()
        if is_it_milk != None:
            milk = is_it_milk
            
