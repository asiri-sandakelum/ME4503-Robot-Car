# test/wifi_test.py
# Verify Pico W connects to WiFi and prints its IP address.

import network
import utime
import sys
sys.path.append('/firmware')
from config import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print(f"Connecting to '{WIFI_SSID}'", end="")
for i in range(20):
    if wlan.isconnected():
        break
    utime.sleep(0.5)
    print(".", end="")

print()
if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print(f"✅ Connected! IP: {ip}")
    print(f"   Open on phone: http://{ip}/")
else:
    print("❌ Failed to connect")
    print("   Check WIFI_SSID and WIFI_PASSWORD in config.py")
