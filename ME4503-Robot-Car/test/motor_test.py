# test/motor_test.py
# Run this FIRST to verify motor wiring before anything else.
# Upload only config.py and motor.py alongside this file.

import sys
sys.path.append('/firmware')
from motor import MotorDriver
from utime import sleep

m = MotorDriver()

print("Test 1: Forward 2s")
m.forward(60); sleep(2); m.stop(); sleep(1)

print("Test 2: Backward 2s")
m.backward(60); sleep(2); m.stop(); sleep(1)

print("Test 3: Turn Left 1s")
m.turn_left(50); sleep(1); m.stop(); sleep(1)

print("Test 4: Turn Right 1s")
m.turn_right(50); sleep(1); m.stop(); sleep(1)

print("Test 5: Set individual speeds (L=80, R=40)")
m.set_motors(80, 40); sleep(2); m.stop()

print("All motor tests complete!")
