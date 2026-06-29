# ============================================================
# wifi_control.py — WiFi Web Server for Mobile App Control
# No app install needed — open http://<pico-ip>/ in phone browser.
# ============================================================

import network
import socket
import utime
from config import WIFI_SSID, WIFI_PASSWORD, SERVER_PORT, State

HTML = """<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ME4503 Robot</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: sans-serif; background: #111; color: #fff; text-align: center; padding: 20px; }
    h2 { margin: 16px 0 8px; font-size: 20px; }
    #status { color: #0af; font-size: 13px; margin: 8px 0 16px; min-height: 18px; }
    .row { display: flex; justify-content: center; gap: 12px; margin: 8px 0; }
    .btn {
      width: 72px; height: 72px; font-size: 28px;
      border-radius: 14px; border: none; cursor: pointer;
      background: #0af; color: #000; font-weight: bold;
    }
    .btn:active { background: #088; }
    .wide { width: 160px; height: 52px; font-size: 15px; background: #f80; }
    .red  { background: #e33; color: #fff; }
    .sep  { margin: 16px 0 8px; border-top: 1px solid #333; padding-top: 12px; font-size: 12px; color: #666; }
    input[type=range] { width: 80%; margin: 8px auto; display: block; }
  </style>
</head>
<body>
  <h2>🤖 ME4503 Robot Car</h2>
  <div id="status">Ready</div>

  <div class="row">
    <button class="btn wide" onclick="cmd('auto')">▶ AUTO MODE</button>
    <button class="btn wide red" onclick="cmd('manual')">🕹 MANUAL</button>
  </div>

  <div class="sep">MANUAL CONTROL</div>

  <div class="row">
    <button class="btn" onclick="cmd('forward')">▲</button>
  </div>
  <div class="row">
    <button class="btn" onclick="cmd('left')">◀</button>
    <button class="btn red" onclick="cmd('stop')">■</button>
    <button class="btn" onclick="cmd('right')">▶</button>
  </div>
  <div class="row">
    <button class="btn" onclick="cmd('backward')">▼</button>
  </div>

  <div class="sep">WALL DISTANCE: <span id="wdval">25</span> cm</div>
  <input type="range" min="20" max="40" value="25" id="wd"
    oninput="document.getElementById('wdval').innerText=this.value"
    onchange="cmd('wall_dist_' + this.value)">

  <script>
    async function cmd(action) {
      try {
        const r = await fetch('/cmd?action=' + action);
        document.getElementById('status').innerText = await r.text();
      } catch(e) {
        document.getElementById('status').innerText = 'Connection error';
      }
    }
  </script>
</body>
</html>"""


class WiFiController:
    def __init__(self, motor, state_machine, wall_follower):
        self.motor = motor
        self.sm    = state_machine
        self.wall  = wall_follower
        self.ip    = None

    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        print("Connecting to WiFi", end="")
        for _ in range(20):
            if wlan.isconnected():
                break
            utime.sleep(0.5)
            print(".", end="")
        if wlan.isconnected():
            self.ip = wlan.ifconfig()[0]
            print(f"\nConnected! Open: http://{self.ip}/")
        else:
            print("\nWiFi failed — running without app control")
        return self.ip

    def handle_request(self, request_str):
        if '/cmd?action=' in request_str:
            action = request_str.split('/cmd?action=')[1].split(' ')[0].strip()

            if   action == 'forward':  self.motor.forward()
            elif action == 'backward': self.motor.backward()
            elif action == 'left':     self.motor.turn_left()
            elif action == 'right':    self.motor.turn_right()
            elif action == 'stop':     self.motor.stop()
            elif action == 'auto':
                self.motor.stop()
                self.sm.transition(State.LINE_FOLLOW)
            elif action == 'manual':
                self.motor.stop()
                self.sm.transition(State.MANUAL)
            elif action.startswith('wall_dist_'):
                d = int(action.split('_')[-1])
                self.wall.set_target(d)
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nWall target: {d} cm"

            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{action} OK"

        return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{HTML}"

    def start_server(self):
        addr = socket.getaddrinfo('0.0.0.0', SERVER_PORT)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        s.setblocking(False)
        print(f"Server running at http://{self.ip}/")
        return s
