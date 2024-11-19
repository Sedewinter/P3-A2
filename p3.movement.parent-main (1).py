from microbit import *
import radio

radio.on()
key = "Key"

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
      
receive()
