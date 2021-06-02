import RPi.GPIO as GPIO 
import time

class PORT:
    UP      = 6
    DOWN    = 13
    ESC     = 19
    ENTER   = 26

channels = [6,13,19,26]

def init_keys():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT.UP,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PORT.DOWN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PORT.ESC,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PORT.ENTER,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(PORT.ESC,GPIO.FALLING,bouncetime=200)
    GPIO.add_event_detect(PORT.DOWN,GPIO.FALLING,bouncetime=200)
    GPIO.add_event_detect(PORT.UP,GPIO.FALLING,bouncetime=200)
    GPIO.add_event_detect(PORT.ENTER,GPIO.FALLING,bouncetime=200)

def query_key():
    
    if GPIO.event_detected(PORT.UP):
        return PORT.UP
    elif GPIO.event_detected(PORT.DOWN):
        return PORT.DOWN
    elif GPIO.event_detected(PORT.ESC):
        return PORT.ESC
    elif GPIO.event_detected(PORT.ENTER):
        return PORT.ENTER
    return None