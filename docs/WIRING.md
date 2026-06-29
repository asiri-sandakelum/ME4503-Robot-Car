# Wiring Guide — ME4503 Robot Car

## ⚠️ Important: HC-SR04 Echo Pin Voltage Divider
HC-SR04 ECHO outputs **5V** but Pico W GPIO is **3.3V max**.
Use a voltage divider: 1kΩ (ECHO → GPIO) + 2kΩ (GPIO → GND).

---

## L298N Motor Driver → Pico W

| L298N Pin | Pico W GPIO | Notes |
|---|---|---|
| IN1 | GP0 | Left motor forward |
| IN2 | GP1 | Left motor backward |
| ENA | GP4 | Left motor PWM speed |
| IN3 | GP2 | Right motor forward |
| IN4 | GP3 | Right motor backward |
| ENB | GP5 | Right motor PWM speed |
| GND | GND | Common ground |
| VCC (5V) | VSYS or 5V rail | Logic power |
| VIN (motor) | Battery+ via switch | Motor power (7.4V) |

---

## 5-Channel IR Line Sensor Array → Pico W

| Sensor Pin | Pico W GPIO |
|---|---|
| S1 (far left) | GP6 |
| S2 | GP7 |
| S3 (centre) | GP8 |
| S4 | GP9 |
| S5 (far right) | GP10 |
| VCC | 3.3V |
| GND | GND |

---

## HC-SR04 Ultrasonic (Front — Obstacle Detection)

| HC-SR04 | Pico W GPIO |
|---|---|
| TRIG | GP14 |
| ECHO | GP15 (via voltage divider!) |
| VCC | 5V rail |
| GND | GND |

---

## HC-SR04 (Left Side — Wall Following)

| HC-SR04 | Pico W GPIO |
|---|---|
| TRIG | GP16 |
| ECHO | GP17 (via voltage divider!) |
| VCC | 5V rail |
| GND | GND |

---

## Power System

```
7.4V Li-ion Battery
        │
        ├──► L298N VIN (motor power)
        │
        └──► Buck Converter (LM2596) → 5V
                    │
                    ├──► Pico W VSYS pin
                    ├──► HC-SR04 (both) VCC
                    └──► L298N VCC (logic)

IR Sensor → Pico W 3.3V (from 3V3 OUT pin)
```

---

## Quick Assembly Checklist

- [ ] Motors wired to L298N output terminals
- [ ] L298N logic pins connected to Pico W (GP0–GP5)
- [ ] ENA and ENB jumpers **removed** (PWM control enabled)
- [ ] IR sensor centred under chassis, facing down
- [ ] Front ultrasonic at robot's front, horizontal
- [ ] Side ultrasonic on LEFT side, horizontal, pointing left
- [ ] Voltage dividers on both ECHO pins
- [ ] Common GND across all components
- [ ] Battery connected through a power switch
