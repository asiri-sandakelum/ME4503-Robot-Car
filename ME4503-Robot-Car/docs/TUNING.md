# Tuning Guide — ME4503 Robot Car

All parameters are in `firmware/config.py`.

---

## Line Following PID

### Starting Values
```python
KP = 0.4
KI = 0.0
KD = 0.1
BASE_SPEED = 60
```

### Tuning Procedure (do in order)
1. Set `KI = 0`, `KD = 0`. Increase `KP` until robot oscillates wildly.
2. Reduce `KP` to ~60% of that value.
3. Increase `KD` slowly until oscillation dampens on curves.
4. `KI` is usually not needed — only add if robot drifts off-centre on long straights.

### Symptom → Fix Table

| Symptom | Fix |
|---|---|
| Wild zigzagging | Reduce KP |
| Too slow to correct on curves | Increase KP |
| Overshoots corners | Increase KD |
| Slow drift off centre | Add small KI (0.001–0.01) |
| Robot too slow overall | Increase BASE_SPEED |
| Robot too fast to control | Reduce BASE_SPEED |

---

## Wall Following

### Examiner sets d during evaluation (20–40 cm)
Use the slider in the mobile app browser, or set it directly:
```python
# In config.py
WALL_DISTANCE_CM = 30   # Change to examiner's value
```

Or call at runtime via app slider (already wired in wifi_control.py).

### WALL_KP Tuning

| Symptom | Fix |
|---|---|
| Robot drifts away from wall slowly | Increase WALL_KP |
| Robot oscillates back and forth | Reduce WALL_KP |

---

## Turn Duration Calibration

The junction scanning uses timed turns. Calibrate for your robot:

```python
# In state_machine.py JUNCTION state
turns = [
    ('forward', 0),
    ('right',   500),   # Adjust until ~90° turn
    ...
]
```

Test with `motor_test.py`: time how long a 90° turn takes at `TURN_SPEED`.

---

## Obstacle Detection Threshold

```python
OBSTACLE_THRESHOLD_CM = 20   # Detect obstacles closer than 20 cm
SCAN_DISTANCE_CM      = 30   # Junction path considered "clear" if > 30 cm
```

Increase `SCAN_DISTANCE_CM` if robot incorrectly reads blocked paths as clear.
