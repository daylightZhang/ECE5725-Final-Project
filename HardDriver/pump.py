# Pump Driver 
# Author: Jingkai Zhang (initialization, set control parameter)
#         Lanyue Fang (choose GPIO port, physical connection)
import RPi.GPIO as GPIO 
import time

class Pump(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)                  # repeat in Motor class
        GPIO.setwarnings(False)
        self.channel = 26
        GPIO.setup(self.channel, GPIO.OUT)      # set GPIO as PWM output
        self.PWM = GPIO.PWM(self.channel, 50)   # set the frequency 50 Hz

    def __del__(self):
        GPIO.cleanup()
    
    def pick(self,motor):
        motor.move('z', -1.5)                     # downwards
        time.sleep(1)
        self.PWM.start(60)
        time.sleep(1)
        motor.move('z', 2)                      # upwards

    def release(self,motor):     
        motor.move('z', -2)                     # downwards
        time.sleep(1)
        self.PWM.stop()
        time.sleep(1)
        motor.move('z', 1.5)                      # upwards
