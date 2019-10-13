import RPi.GPIO as GPIO
import time


class ExtraChallenge:
    enabled = True
    started = False

    def __init__(self):
        self.stop_callback = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(40, GPIO.OUT)
        GPIO.output(40, GPIO.LOW)

        GPIO.setup(38, GPIO.OUT)
        GPIO.output(38, GPIO.LOW)

        GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def stop_cb(self, channel):
        self.stop()
        if self.stop_callback:
            self.stop_callback()

    def start(self, stop_callback):
        if self.started:
            return
        self.started = True
        self.stop_callback = stop_callback
        GPIO.output(40, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(40, GPIO.LOW)
        GPIO.add_event_detect(37, GPIO.RISING, callback=self.stop_cb)

    def stop(self):
        if not self.started:
            return
        self.started = False

        GPIO.remove_event_detect(37)
        GPIO.output(38, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(38, GPIO.LOW)
