# ============================================================
# state_machine.py — Robot Finite State Machine
#
# States:
#   MANUAL         → WiFi app controls motors directly
#   LINE_FOLLOW    → PID line following, monitors for obstacles/junctions
#   OBSTACLE_CHECK → Scans directions, picks free path at junction
#   WALL_FOLLOW    → Dead-zone: follow left wall until line reappears
#   JUNCTION       → 4-way junction: scan all paths, pick clear one
#   STOP           → Final stop at end of path
# ============================================================

from config import State, OBSTACLE_THRESHOLD_CM, SCAN_DISTANCE_CM
from utime import sleep_ms

class RobotStateMachine:
    def __init__(self, motor, line_sensor, ultrasonic, wall_follower):
        self.motor  = motor
        self.line   = line_sensor
        self.sonic  = ultrasonic
        self.wall   = wall_follower
        self.state  = State.MANUAL

    def transition(self, new_state):
        print(f"[FSM] {self.state} → {new_state}")
        self.state = new_state

    def run(self):
        """Call this every loop iteration."""

        # ── MANUAL ───────────────────────────────────────────
        if self.state == State.MANUAL:
            # Motors controlled by WiFi handler externally
            pass

        # ── LINE FOLLOW ──────────────────────────────────────
        elif self.state == State.LINE_FOLLOW:
            # Check for obstacle ahead
            if self.sonic.obstacle_detected():
                self.motor.stop()
                self.transition(State.OBSTACLE_CHECK)
                return

            left, right = self.line.compute_pid()

            if left is None:
                # Line lost
                if self.line.is_junction():
                    self.transition(State.OBSTACLE_CHECK)
                else:
                    # Could be dead zone — switch to wall follow
                    self.transition(State.WALL_FOLLOW)
                return

            self.motor.set_motors(left, right)

        # ── OBSTACLE CHECK (1st junction) ────────────────────
        elif self.state == State.OBSTACLE_CHECK:
            self.motor.stop()
            sleep_ms(300)

            # Try forward first
            if self.sonic.get_distance_cm() > SCAN_DISTANCE_CM:
                self.motor.forward()
                sleep_ms(400)
                self.transition(State.LINE_FOLLOW)
                return

            # Try right
            self.motor.turn_right()
            sleep_ms(500)
            self.motor.stop()
            sleep_ms(200)
            if self.sonic.get_distance_cm() > SCAN_DISTANCE_CM:
                self.motor.forward()
                sleep_ms(400)
                self.transition(State.LINE_FOLLOW)
                return

            # Try left (rotate back past centre then left)
            self.motor.turn_left()
            sleep_ms(1000)
            self.motor.stop()
            sleep_ms(200)
            self.transition(State.LINE_FOLLOW)

        # ── WALL FOLLOW (dead zone) ──────────────────────────
        elif self.state == State.WALL_FOLLOW:
            left, right, dist = self.wall.compute()
            self.motor.set_motors(left, right)

            # Line reappeared → 4-way junction coming up
            if self.line.get_position() is not None:
                self.transition(State.JUNCTION)

        # ── JUNCTION (4-way, end of wall section) ────────────
        elif self.state == State.JUNCTION:
            self.motor.stop()
            sleep_ms(400)

            # Scan 4 directions: forward, right, back, left
            turns = [
                ('forward', 0),
                ('right',   500),   # ~90° right turn duration ms
                ('back',    500),   # another 90° = 180° total
                ('left',    500),   # another 90° = 270° total (left of start)
            ]

            for direction, turn_ms in turns:
                if turn_ms > 0:
                    self.motor.turn_right()
                    sleep_ms(turn_ms)
                    self.motor.stop()
                    sleep_ms(300)

                dist = self.sonic.get_distance_cm()
                print(f"  Scanning {direction}: {dist} cm")

                if dist > SCAN_DISTANCE_CM:
                    print(f"  Clear path → {direction}")
                    self.motor.forward()
                    sleep_ms(400)
                    self.transition(State.LINE_FOLLOW)
                    return

            # All paths blocked (shouldn't happen in eval)
            print("All paths blocked — stopping")
            self.transition(State.STOP)

        # ── STOP ─────────────────────────────────────────────
        elif self.state == State.STOP:
            self.motor.stop()
