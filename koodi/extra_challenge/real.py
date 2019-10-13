import RPi.GPIO as GPIO
import time

class ExtraChallenge:
    enabled = True
    started = False

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)

    def start(self):
        if self.started:
            return
        self.started = True

        GPIO.output(12, GPIO.HIGH)
        time.sleep(200)
        GPIO.output(12, GPIO.LOW)

    def stop(self):
        if not self.started:
            return
        self.started = False