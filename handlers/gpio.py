from typing import Final

import RPi.GPIO as GPIO
import time


class GpioHandler:
    """
    라즈베리파이 GPIO 핸들러.
    """
    RADIAL_BTN: Final[int] = 5
    PAIRING_BTN: Final[int] = 6
    
    def setup(self):
        """
        GPIO핀 세팅.
        :return:
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RADIAL_BTN, GPIO.OUT)
        GPIO.setup(PAIRING_BTN, GPIO.IN)


    def loop(self):
        """
        아두이노와 같은 loop.
        """
        

    def teardown(self):
        """
        종료.
        """
        GPIO.cleanup()
    
    def __del__(self):
        self.teardown()