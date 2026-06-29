# ============================================================
# ultrasonic.py — HC-SR04 Ultrasonic Distance Sensor
# ⚠️  ECHO pin outputs 5V — use a voltage divider to 3.3V!
#     1kΩ (ECHO→GPIO) + 2kΩ (GPIO→GND)
# ============================================================

from machine import Pin, time_pulse_us
from utime import sleep_us
from config import ULTRASONIC_TRIG, ULTRASONIC_ECHO, OBSTACLE_THRESHOLD_CM

class Ultrasonic:
    def __init__(self, trig_pin=ULTRASONIC_TRIG, echo_pin=ULTRASONIC_ECHO):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trig.low()

    def get_distance_cm(self):
        """
        Trigger a measurement and return distance in cm.
        Returns 999 on timeout (no obstacle in range).
        """
        self.trig.low()
        sleep_us(2)
        self.trig.high()
        sleep_us(10)
        self.trig.low()

        duration = time_pulse_us(self.echo, 1, 30000)  # 30ms timeout
        if duration < 0:
            return 999

        return round((duration / 2) / 29.1, 1)

    def obstacle_detected(self, threshold=OBSTACLE_THRESHOLD_CM):
        """Returns True if obstacle is closer than threshold cm."""
        return self.get_distance_cm() < threshold
