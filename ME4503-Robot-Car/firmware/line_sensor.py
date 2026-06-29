# ============================================================
# line_sensor.py — 5-Channel IR Line Sensor + PID Controller
# ============================================================

from machine import Pin
from config import *

class LineSensor:
    def __init__(self):
        self.sensors  = [Pin(p, Pin.IN) for p in IR_PINS]
        self.weights  = [-2, -1, 0, 1, 2]  # Position weights L→R
        self.last_error = 0
        self.integral   = 0

    def read(self):
        """Returns list of 5 values: 1 = on black line, 0 = off."""
        return [s.value() if LINE_DARK_VALUE == 1 else 1 - s.value()
                for s in self.sensors]

    def get_position(self):
        """
        Weighted average position error.
        0 = centred, negative = line is left, positive = line is right.
        Returns None if no line detected (line lost).
        """
        vals  = self.read()
        total = sum(vals)
        if total == 0:
            return None
        return sum(v * w for v, w in zip(vals, self.weights)) / total

    def is_junction(self):
        """4 or more sensors on line = junction detected."""
        return sum(self.read()) >= 4

    def is_line_end(self):
        """All sensors off line = end of path."""
        return sum(self.read()) == 0

    def compute_pid(self):
        """
        Compute PID correction and return (left_speed, right_speed).
        Returns (None, None) if line is lost.
        """
        error = self.get_position()
        if error is None:
            return None, None

        self.integral  += error
        derivative      = error - self.last_error
        self.last_error = error

        correction = KP * error + KI * self.integral + KD * derivative

        left  = BASE_SPEED + correction * 30
        right = BASE_SPEED - correction * 30

        left  = max(0, min(100, left))
        right = max(0, min(100, right))

        return left, right
