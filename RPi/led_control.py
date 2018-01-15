import RPi.GPIO as GPIO
import time
import pigpio

'''
Pins:
Strip1:4,17,27
Strip2:22,18,23
Strip3:5,6,13
Strip4:16,20,21
'''

class StripControl():

    def __init__(self):
        self.brightness = 1
        self.gpio = pigpio.pi()

        #self.gpio.set_PWM_frequency()
        # One of these:  8000  4000  2000 1600 1000  800  500  400  320
        #    250   200   160  100   80   50   40   20   10

        self.strips = [[4,17,27],[22,18,23],[5,6,13],[16,20,21]]
        self.strip_colors = [[100,100,100],[100,100,100],[100,100,100],[100,100,100]]

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
            for ledidx, ledPin in enumerate(strip):
                gpio.set_PWM_dutycycle(ledPin, int(self.strip_colors[sidx][ledidx]*self.brightness))

    def stop(self):
        self.gpio.stop()


if __name__ == "__main__":
        strip = StripControl()
        time.sleep(2)
        strip.setStripColor(0, (200,100,0))
        time.sleep(10)
        strip.stop()
