# ME4503 — Autonomous Robot Car

A Raspberry Pi Pico W-based autonomous robot for the ME4503 Mechatronics System Design module at the University of Moratuwa.

## Capabilities

| Feature | Status |
|---|---|
| Mobile App Control (WiFi browser) | Done |
| Line Following (PID, 5-sensor IR) | Done |
| Obstacle Avoidance at Junctions | Done |
| Wall Following (proportional control) | Done |
| Autonomous 4-way Junction Decision | Done |
| Auto Stop at Path End | Done |

## Hardware

| Component | Model |
|---|---|
| Microcontroller | Raspberry Pi Pico W |
| Motor Driver | L298N / TB6612FNG |
| Line Sensor | 5-channel IR array |
| Obstacle Sensor | HC-SR04 (front) |
| Wall Sensor | HC-SR04 (left side) |
| Battery | 7.4V Li-ion 2S |
| Buck Converter | LM2596 7.4V to 5V |

## Pin Map

| Function | GPIO |
|---|---|
| Motor L IN1, IN2 | GP0, GP1 |
| Motor R IN1, IN2 | GP2, GP3 |
| Motor L/R PWM | GP4, GP5 |
| IR Sensors S1-S5 | GP6-GP10 |
| Ultrasonic front TRIG/ECHO | GP14, GP15 |
| Wall sensor TRIG/ECHO | GP16, GP17 |

> HC-SR04 ECHO outputs 5V. Use 1k+2k voltage divider before Pico GPIO.

## Firmware

```
firmware/
  main.py          Entry point
  config.py        All tunable parameters
  motor.py         Motor driver
  line_sensor.py   IR sensor + PID
  ultrasonic.py    HC-SR04 driver
  wall_follow.py   Wall following controller
  state_machine.py Finite state machine
  wifi_control.py  WiFi web app
```

## Quick Start

1. Flash MicroPython onto Pico W (micropython.org/download/rp2-pico-w)
2. Edit WIFI_SSID and WIFI_PASSWORD in config.py
3. Upload all firmware/ files to Pico W (Thonny or mpremote)
4. Run test/motor_test.py first, then sensor_test.py
5. Run main.py - Pico W prints its IP
6. Open http://<ip>/ on phone browser to control robot

## Docs

- docs/WIRING.md - Full wiring guide
- docs/TUNING.md - PID and wall distance tuning

## Module

ME4503 Mechatronics System Design
Department of Mechanical Engineering, University of Moratuwa
