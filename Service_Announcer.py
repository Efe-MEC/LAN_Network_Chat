import socket
import json
import time

user_name = input("Enter your username: ")

my_ip = socket.gethostbyname(socket.gethostname())

message_data = {
    "username": user_name,
}
message_json = json.dumps(message_data)

broadcast_ip = '25.255.255.255'
broadcast_port = 6000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"Broadcasting from {my_ip}")

while True:

	sock.sendto(message_json.encode(), (broadcast_ip, broadcast_port))

	time.sleep(8)

sock.close()
