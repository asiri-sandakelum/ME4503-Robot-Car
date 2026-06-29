# ============================================================
# config.py — ME4503 Robot Car
# All tunable parameters in one place.
# Edit this file to tune behaviour without touching other modules.
# ============================================================

# --- WiFi (for mobile app control) ---
WIFI_SSID = "YOUR_SSID"
WIFI_PASSWORD = "YOUR_PASSWORD"
SERVER_PORT = 80

# --- Motor Pins (L298N / TB6612) ---
MOTOR_LEFT_IN1  = 0   # GP0
MOTOR_LEFT_IN2  = 1   # GP1
MOTOR_LEFT_PWM  = 4   # GP4 (ENA)

MOTOR_RIGHT_IN1 = 2   # GP2
MOTOR_RIGHT_IN2 = 3   # GP3
MOTOR_RIGHT_PWM = 5   # GP5 (ENB)

# --- IR Line Sensor Pins (5-channel, left to right) ---
IR_PINS = [6, 7, 8, 9, 10]   # GP6–GP10
LINE_DARK_VALUE = 1           # 1 if sensor reads HIGH on black line

# --- Ultrasonic Sensor Pins (Front - Obstacle) ---
ULTRASONIC_TRIG = 14   # GP14
ULTRASONIC_ECHO = 15   # GP15

# --- Wall Sensor Pins (Side - Wall Following) ---
WALL_SENSOR_TRIG = 16  # GP16
WALL_SENSOR_ECHO = 17  # GP17

# --- Base Motor Speeds (0-100 %) ---
BASE_SPEED  = 60
TURN_SPEED  = 50
WALL_SPEED  = 50

# --- PID Gains for Line Following ---
KP = 0.4
KI = 0.0
KD = 0.1

# --- Wall Following ---
WALL_DISTANCE_CM = 25   # Target distance (20-40 cm, set by examiner)
WALL_KP = 1.2

# --- Obstacle Detection ---
OBSTACLE_THRESHOLD_CM = 20
SCAN_DISTANCE_CM      = 30

# --- States ---
class State:
    MANUAL         = "MANUAL"
    LINE_FOLLOW    = "LINE_FOLLOW"
    OBSTACLE_CHECK = "OBSTACLE_CHECK"
    WALL_FOLLOW    = "WALL_FOLLOW"
    JUNCTION       = "JUNCTION"
    STOP           = "STOP"
