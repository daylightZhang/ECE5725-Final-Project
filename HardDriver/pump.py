# Pump Driver 
# Author: Jingkai Zhang (initialization, set control parameter)
#         Lanyue Fang (choose GPIO port, physical connection)
import RPi.GPIO as GPIO 

class Pump(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # repeat in Motor class
        GPIO.setwarnings(False)
        self.channel = 26
        GPIO.setup(self.channel, GPIO.OUT)  # set GPIO as PWM output
        self.PWM = GPIO.PWM(self.channel, 50)  # set the frequency 50 Hz

    def __del__(self):
        GPIO.cleanup()

    def pick(self):
        self.PWM.start(60)

    def drop(self):
        self.PWM.stop()

