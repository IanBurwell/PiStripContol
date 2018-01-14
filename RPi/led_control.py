import RPi.GPIO as GPIO
import time
'''
Pins:
Strip1:7,11,13
Strip2:15,12,16
Strip3:29,31,33
Strip4:36,38,40
'''

class StripControll():


    __init__(self):
        self.frequency = 1000
        self. brightness = 100

        GPIO.setmode(GPIO.BOARD)
        self.strips = [(GPIO.PWM(7, frequency),GPIO.PWM(11, frequency),GPIO.PWM(13, frequency)),
                (GPIO.PWM(29, frequency),GPIO.PWM(31, frequency),GPIO.PWM(33, frequency)),
                (GPIO.PWM(36, frequency),GPIO.PWM(38, frequency),GPIO.PWM(40, frequency))]

        for strip in self.strips:
            for color in strip:
                color.start(100)
                #pwm.ChangeDutyCycle(75)

    def setState(bright=None):
        if bright is not None:
            self.brightness = bright

    def setStripColor(index, color):
        strip = self.strips[index]
