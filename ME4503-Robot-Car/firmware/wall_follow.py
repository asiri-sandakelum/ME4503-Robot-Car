# ============================================================
# wall_follow.py — Wall Following Controller
# Proportional control to maintain target distance from wall.
# Wall assumed on the LEFT side of the robot.
# ============================================================

from ultrasonic import Ultrasonic
from config import WALL_SENSOR_TRIG, WALL_SENSOR_ECHO, WALL_DISTANCE_CM, WALL_KP, WALL_SPEED

class WallFollower:
    def __init__(self):
        self.sensor = Ultrasonic(trig_pin=WALL_SENSOR_TRIG, echo_pin=WALL_SENSOR_ECHO)
        self.target = WALL_DISTANCE_CM

    def set_target(self, distance_cm):
        """
        Call this when examiner specifies the wall distance (20-40 cm).
        Example: wall.set_target(30)
        """
        self.target = distance_cm
        print(f"Wall target set to {distance_cm} cm")

    def compute(self):
        """
        Returns (left_speed, right_speed, current_distance).
        Positive error = too far from wall → steer left (toward wall).
        Negative error = too close → steer right (away from wall).
        """
        distance = self.sensor.get_distance_cm()
        error    = distance - self.target   # + = too far, - = too close

        correction = WALL_KP * error

        left  = WALL_SPEED - correction   # Reduce left to turn toward wall
        right = WALL_SPEED + correction   # Increase right to compensate

        left  = max(20, min(100, left))
        right = max(20, min(100, right))

        return left, right, distance
