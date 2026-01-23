import subprocess
import re
from collections import defaultdict

networks = defaultdict(set)

output = subprocess.check_output(
    ["netsh", "wlan", "show", "networks", "mode=bssid"],
    encoding="utf-8"
)

current_ssid = None

for line in output.splitlines():
    ssid_match = re.search(r"SSID\s+\d+\s+:\s(.+)", line)
    bssid_match = re.search(r"BSSID\s+\d+\s+:\s(.+)", line)

    if ssid_match:
        current_ssid = ssid_match.group(1).strip()

    if bssid_match and current_ssid:
        networks[current_ssid].add(bssid_match.group(1).strip())

for ssid, macs in networks.items():
    if len(macs) > 1:
        print("⚠️ POSSIBLE EVIL TWIN DETECTED")
        print(f"SSID: {ssid}")
        print(f"MAC Addresses: {macs}\n")
