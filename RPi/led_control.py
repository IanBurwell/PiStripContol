import RPi.GPIO as GPIO
import time
'''
Pins:
Strip1:4,17,27
Strip2:22,18,23
Strip3:5,6,13
Strip4:16,20,21
'''

class StripControl():

    def __init__(self):
        self.frequency = 100
        self.brightness = 1

        GPIO.setmode(GPIO.BCM)
        for pin in [4,17,27,22,18,23,5,6,13,16,20,21]:
            GPIO.setup(pin, GPIO.OUT)
        self.strips = [[GPIO.PWM(4, self.frequency),GPIO.PWM(17, self.frequency),GPIO.PWM(27, self.frequency)],
                [GPIO.PWM(22, self.frequency),GPIO.PWM(18, self.frequency),GPIO.PWM(23, self.frequency)],
                [GPIO.PWM(5, self.frequency),GPIO.PWM(6, self.frequency),GPIO.PWM(13, self.frequency)],
                [GPIO.PWM(16, self.frequency),GPIO.PWM(20, self.frequency),GPIO.PWM(21, self.frequency)]]

        self.strip_colors = [[100,100,100],[100,100,100],[100,100,100],[100,100,100]]

        for strip in self.strips:
            for color in strip:
                color.start(100)
                #pwm.ChangeDutyCycle(75)

    def setState(self, bright=None):
        if bright is not None:
            self.brightness = double(bright if 1>= bright >=0 else 0.75)

    def setStripColor(self, index, color):
        r,g,b = color
        self.strip_colors[index] = [int(r/2.55),int(g/2.55),int(b/2.55)]
        self.update()

    def update(self):
        print(self.strip_colors)
        for sidx, strip in enumerate(self.strips):
            for ledidx, led in enumerate(strip):
                led.ChangeDutyCycle(int(self.strip_colors[sidx][ledidx]*self.brightness))

    def stop(self):
        for strip in self.strips:
            for pwm in strip:
                pwm.stop()


if __name__ == "__main__":
        strip = StripControl()
        time.sleep(2)
        strip.setStripColor(0, (200,100,0))
        time.sleep(10)
        strip.stop()
