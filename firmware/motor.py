# ============================================================
# motor.py — Motor Driver Abstraction
# Supports L298N and TB6612FNG wiring with PWM speed control.
# ============================================================

from machine import Pin, PWM
from config import *

class MotorDriver:
    def __init__(self):
        # Left motor
        self.left_in1 = Pin(MOTOR_LEFT_IN1, Pin.OUT)
        self.left_in2 = Pin(MOTOR_LEFT_IN2, Pin.OUT)
        self.left_pwm = PWM(Pin(MOTOR_LEFT_PWM))
        self.left_pwm.freq(1000)

        # Right motor
        self.right_in1 = Pin(MOTOR_RIGHT_IN1, Pin.OUT)
        self.right_in2 = Pin(MOTOR_RIGHT_IN2, Pin.OUT)
        self.right_pwm = PWM(Pin(MOTOR_RIGHT_PWM))
        self.right_pwm.freq(1000)

    def _duty(self, speed):
        """Convert speed (0-100) to 16-bit duty cycle."""
        return int(min(max(speed, 0), 100) / 100 * 65535)

    def set_motors(self, left_speed, right_speed):
        """
        Set individual motor speeds.
        Positive = forward, Negative = backward, 0 = stop.
        Range: -100 to 100
        """
        # Left motor direction
        if left_speed > 0:
            self.left_in1.high(); self.left_in2.low()
        elif left_speed < 0:
            self.left_in1.low(); self.left_in2.high()
        else:
            self.left_in1.low(); self.left_in2.low()
        self.left_pwm.duty_u16(self._duty(abs(left_speed)))

        # Right motor direction
        if right_speed > 0:
            self.right_in1.high(); self.right_in2.low()
        elif right_speed < 0:
            self.right_in1.low(); self.right_in2.high()
        else:
            self.right_in1.low(); self.right_in2.low()
        self.right_pwm.duty_u16(self._duty(abs(right_speed)))

    def forward(self, speed=None):
        s = speed if speed is not None else BASE_SPEED
        self.set_motors(s, s)

    def backward(self, speed=None):
        s = speed if speed is not None else BASE_SPEED
        self.set_motors(-s, -s)

    def turn_left(self, speed=None):
        s = speed if speed is not None else TURN_SPEED
        self.set_motors(-s, s)

    def turn_right(self, speed=None):
        s = speed if speed is not None else TURN_SPEED
        self.set_motors(s, -s)

    def stop(self):
        self.set_motors(0, 0)
