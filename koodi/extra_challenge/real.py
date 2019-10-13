import RPi.GPIO as GPIO
import time

class ExtraChallenge:
    enabled = True
    started = False

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)

    def start(self):
        if self.started:
            return
        self.started = True

        GPIO.output(40, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(40, GPIO.LOW)

    def stop(self):
        if not self.started:
            return
        self.started = False