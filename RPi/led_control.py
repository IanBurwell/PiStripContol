import time
import pigpio
import threading
import helpers

'''
Pins:
Strip1:4,17,27
Strip2:22,18,23
Strip3:5,6,13
Strip4:16,20,21
'''

class SequenceThread(threading.Thread):
    def __init__(self, strip_control):
        threading.Thread.__init__(self)
        self.sc = strip_control
        self.stop_event = threading.Event()
        self.daemon = True  # OK for main to exit even if instance is still running. kills thread when main prog exits
        self.paused = True  # start out paused
        self.state = threading.Condition()
        self.sequence = None


    def run(self):
        self.pause()
        i = 0
        while not self.stop_event.is_set():
            with self.state:
                if self.paused:
                    self.state.wait()
            #DO STUFF
            if self.sequence is None:
                self.pause()
                time.sleep(0.01)
                continue
            if i > 6:
                i = 0
            else:
                i += 1
            colors = [self.sequence['0'][i],
                self.sequence['1'][i],
                self.sequence['2'][i],
                self.sequence['3'][i]]
            self.sc.update(colors)
            time.sleep(self.sequence['onTime'])

            #CODE TO FADE
            j = i if i < 7 else 0
            nextColors = [self.sequence['0'][i],
                self.sequence['1'][i],
                self.sequence['2'][i],
                self.sequence['3'][i]]
            differences = []
            for idx in range(4):
                differences.append(helpers.colorDifference(nextColors[idx]))

            #find biggest difference, for loop that manny times adding r/largest diff etc to the color channels with time/diff in time.sleep
            maxDist = max(differences)
            for fDist in range(maxDist):
                for idx in range(4):
                    colors[idx] += differences[idx]/maxDist
                if self.paused:
                    break
                self.sc.update(colors)
                time.sleep(self.sequence['fadeTime']/maxDist)


    def resume(self, sequence=None):
        self.sequence = sequence
        with self.state:
            self.paused = False
            self.state.notify()


    def pause(self):
        with self.state:
            self.paused = True


    def stop(self):#not really needed as its a daemon
        self.pause()
        self.stop_event.set()


class StripControl():

    def __init__(self):
        self.brightness = 1
        self.gpio = pigpio.pi()
        self.sequence = SequenceThread(self)
        self.sequence.start()
        #self.gpio.set_PWM_frequency()
        # One of these:  8000  4000  2000 1600 1000  800  500  400  320
        #    250   200   160  100   80   50   40   20   10
        self.strips = [[4,17,27],[22,18,23],[5,6,13],[16,20,21]]
        self.strip_colors = [[100,100,100],[100,100,100],[100,100,100],[100,100,100]]


    def setState(self, bright=None, sequence=None):
        if sequence is not None and not isinstance(sequence, dict):
            raise Exeption("sequence isnt a dictionary")
        if bright is not None:
            self.brightness = double(bright if 1>= bright >=0 else 0.75)
        if sequence is not None:
            self.sequence.resume(sequence)
        else:
            self.sequence.pause()


    def setStripColor(self, index, color):
        self.setState(sequence=None)
        r,g,b = color
        self.strip_colors[index] = [int(r/2.55),int(g/2.55),int(b/2.55)]
        self.update()


    def update(self, colors=None):
        if colors is not None:
            for index, color in enumerate(colors):
                r,g,b = color
                self.strip_colors[index] = [int(r/2.55),int(g/2.55),int(b/2.55)]
        #print(self.strip_colors)
        for sidx, strip in enumerate(self.strips):
            for ledidx, ledPin in enumerate(strip):
                self.gpio.set_PWM_dutycycle(ledPin, int(self.strip_colors[sidx][ledidx]*self.brightness))


    def stop(self):
        for i in range(4):
            self.setStripColor(i, (0,0,0))
        self.setState(sequence=None)
        self.sequence.stop()
        self.gpio.stop()




if __name__ == "__main__":
    strip = StripControl()
    time.sleep(2)
    strip.setStripColor(0, (0,0,0))
    strip.stop()
