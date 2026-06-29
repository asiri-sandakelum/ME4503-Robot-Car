# ============================================================
# main.py — ME4503 Robot Car Entry Point
# Flash all firmware/ files to Pico W, then run this.
# ============================================================

from motor import MotorDriver
from line_sensor import LineSensor
from ultrasonic import Ultrasonic
from wall_follow import WallFollower
from state_machine import RobotStateMachine
from wifi_control import WiFiController
from config import State
import utime

print("=" * 40)
print("ME4503 Autonomous Robot Car")
print("University of Moratuwa")
print("=" * 40)

# --- Initialise all modules ---
motor  = MotorDriver()
line   = LineSensor()
sonic  = Ultrasonic()
wall   = WallFollower()
sm     = RobotStateMachine(motor, line, sonic, wall)
wifi   = WiFiController(motor, sm, wall)

# --- Connect WiFi ---
wifi.connect()
server_socket = wifi.start_server()

print("\nStarting in MANUAL mode.")
print("Open browser on phone to control robot.")
print("Press AUTO on app to begin autonomous run.\n")

# --- Main Loop ---
while True:
    # Non-blocking WiFi request handler
    try:
        conn, addr = server_socket.accept()
        request = conn.recv(1024).decode('utf-8', 'ignore')
        response = wifi.handle_request(request)
        conn.send(response.encode())
        conn.close()
    except OSError:
        pass  # No pending connection

    # Run state machine tick
    sm.run()

    utime.sleep_ms(10)
