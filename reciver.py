import socket
import json
import os
import time

ip_file = "ip.json"

if os.path.exists(ip_file):
    with open(ip_file, "r") as f:
        ips = json.load(f)
else:
	ips = {}
        
broadcast_port = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", broadcast_port))

print(f"Listening on port {broadcast_port}")

while True:
    
    data, addr = sock.recvfrom(1024)
    message = json.loads(data.decode())
    
    name = message["name"]
    ip = message["ip"]
    time_now = time.time()
    
    ips[ip] = {
		"name": name,
		"time": time_now
	}
    
    with open(ip_file, "w") as f:
        json.dump(ips, f, indent=4)
