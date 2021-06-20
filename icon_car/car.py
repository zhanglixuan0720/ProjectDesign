import RPi.GPIO as gpio
import time
import numpy as np

# author: Jiyuan Yang
# API for Car control


class Car:
    def __init__(self):
        # init the pins
        pin1 = 12
        pin2 = 16
        pin3 = 22
        pin4 = 18
        # set GPI0 as BOARD coding rule
        gpio.setmode(gpio.BOARD)
        # set GPIO as output
        gpio.setup(pin1, gpio.OUT)
        gpio.setup(pin2, gpio.OUT)
        gpio.setup(pin3, gpio.OUT)
        gpio.setup(pin4, gpio.OUT)
        # set pwm wave, 500Hz
        self.pwm1 = gpio.PWM(pin1, 500)
        self.pwm2 = gpio.PWM(pin2, 500)
        self.pwm3 = gpio.PWM(pin3, 500)
        self.pwm4 = gpio.PWM(pin4, 500)
        # init pwm wave
        self.pwm1.start(0)
        self.pwm2.start(0)
        self.pwm3.start(0)
        self.pwm4.start(0)

    def __del__(self):
        self.pwm1.stop()
        self.pwm2.stop()
        self.pwm3.stop()
        self.pwm4.stop()
        gpio.cleanup()

    def forward(self):
        self.pwm1.ChangeDutyCycle(25)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm3.ChangeDutyCycle(25)
        self.pwm4.ChangeDutyCycle(0)

    def backward(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(10)
        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(10)

    def turnleft(self, angle):
        angle = angle if angle < 65else 65
        self.pwm1.ChangeDutyCycle(2)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm3.ChangeDutyCycle(35 + angle)
        self.pwm4.ChangeDutyCycle(0)

    def turnright(self, angle):
        angle = angle if angle < 35else 35
        self.pwm1.ChangeDutyCycle(65 + angle)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm3.ChangeDutyCycle(1)
        self.pwm4.ChangeDutyCycle(0)

    def stop(self):
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)
        self.pwm3.ChangeDutyCycle(0)
        self.pwm4.ChangeDutyCycle(0)
