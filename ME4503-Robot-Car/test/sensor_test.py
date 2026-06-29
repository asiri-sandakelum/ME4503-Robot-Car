# test/sensor_test.py
# Verify IR sensor and ultrasonic readings in real time.

import sys
sys.path.append('/firmware')
from line_sensor import LineSensor
from ultrasonic import Ultrasonic
from utime import sleep

line  = LineSensor()
sonic = Ultrasonic()

print("Sensor live readings — place robot on track")
print("Ctrl+C to stop\n")

try:
    while True:
        vals = line.read()
        pos  = line.get_position()
        dist = sonic.get_distance_cm()
        junc = line.is_junction()
        print(f"IR: {vals}  Pos: {str(pos):>6}  Dist: {dist:>5} cm  Junction: {junc}")
        sleep(0.2)
except KeyboardInterrupt:
    print("Done")
