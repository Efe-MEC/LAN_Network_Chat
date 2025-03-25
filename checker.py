import json
import os
import time

data_file = "ip.json"
timeout = 15

while True:
    if not os.path.exists(data_file):
        print("File not found. Waiting for broadcast...")
        time.sleep(10)
        continue

    with open(data_file, "r") as f:
        ips = json.load(f)

    now = time.time()

    for ip, info in ips.items():
        last_seen = info["time"]
        status = "🟢 ONLINE" if (now - last_seen) < timeout else "🔴 OFFLINE"
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_seen))
        print(f"{info['name']} ({ip}) -> {status} (Son mesaj: {formatted_time})")

    time.sleep(10)