import socket
import json
import os
import time
from cryptography.fernet import Fernet

ip_file = "ips.json"

p = 19
g = 2

def load_users():
	if os.path.exists(ip_file):
		with open(ip_file, "r") as f:
			ips = json.load(f)
	else:
		ips = {}
	now = time.time()
	for ip, data in ips.items():
		if now - data["time"] <= 10:
			print(f"{data['name']} (Online)")
		elif now - data["time"] <= 900:
			print(f"{data['name']} (Away)")


def secure_chat(ip):

	print(f"Secure chat selected.")
	private_nbr = input("Please enter the encrypted key number (3 digit) :  \n")

	enc_nbr = (g ** int(private_nbr)) % p

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, 6001))

		message_key = {
    	"key": enc_nbr,
    	}

		message_json = json.dumps(message_key)
		sock.send(json.dumps(message_json).encode())

		print(f"My public key sent: {enc_nbr}, waiting for response key...")
		data = sock.recv(1024).decode()
		peer_public_key = json.loads(data)["key"]
		print(f"Peer public key received: {peer_public_key}")
		peer_common_key = (peer_public_key ** int(private_nbr)) % p
		print(f"Peer private key calculated: {peer_common_key}")


	except socket.error as e:
		print(f"Connection error: {e}")
		return


def unsecure_chat(ip):
	
	print(f"Unsecure chat selected.")
	message_input = input("Please enter your message:\n")

	message = {
	"unencrypted_message": message_input,
	}

	message_json = json.dumps(message)

	try:
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, 6001))

		sock.send(json.dumps(message_json).encode())

		sock.close()
	
	except socket.error as e:
		print(f"Connection error: {e}")


def load_chat():

	in_username = input("Please enter the selected username: \n")
	sec_key = input("Please enter the chat type code: \nSecure Chat (1)\nUnsecure Chat (2)\n")

	if os.path.exists(ip_file):
		with open(ip_file, "r") as f:
			ips = json.load(f)
	else:
		ips = {}

	if sec_key == "1":
		print(f"Secure chat with {in_username} initiated.")
		if in_username in ips:
			ip = ips[in_username]["ip"]
		secure_chat(ip)

	elif sec_key == "2":
		print(f"Unsecure chat with {in_username} initiated.")
		if in_username in ips:
			ip = ips[in_username]["ip"]
		unsecure_chat(ip)
		
	else:
		print("Invalid chat type code. Enter 1 or 2.")


def main ():

	while True:

		op_code = input("Please enter the operation code:\nUsers (1)\nChat (2)\nHistory (3)\n")

		if op_code == "1":
			load_users()
		elif op_code == "2":
			load_chat()
		elif op_code == "3":
			print("History")
		else:
			print("Invalid operation code. Enter 1, 2 or 3.")

if __name__ == "__main__":
	main()