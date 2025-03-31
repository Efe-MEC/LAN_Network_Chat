import socket
import json
import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import base64

ip_file = "ips.json"

p = 19
g = 2

socket_number = 6001

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


def save_log():
	print(f"Saving log...")
	


def fernet_key(key):
	
	hkdf = HKDF(
		algorithm=hashes.SHA256(),
		length=32,
		salt=None,
		info=None,
	)

	key_hdkf = hkdf.derive(str(key).encode())

	fernet_key = base64.urlsafe_b64encode(key_hdkf)
	fernet = Fernet(fernet_key)
	return fernet

def secure_chat(ip):

	print(f"Secure chat selected.")
	private_nbr = input("Please enter the encrypted key number (3 digit) :  \n")

	enc_nbr = (g ** int(private_nbr)) % p

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, socket_number))

		message_key = {
    	"key": enc_nbr,
    	}

		message_json = json.dumps(message_key)
		sock.send(json.dumps(message_json).encode())

		print(f"My public key sent: {enc_nbr}, waiting for response key...")
		data = sock.recv(1024).decode()
		peer_public_key = int(json.loads(data)["key"])
		print(f"Peer public key received: {peer_public_key}")
		peer_common_key = (peer_public_key ** int(private_nbr)) % p
		print(f"Peer common key calculated: {peer_common_key}")

		fernet = fernet_key(peer_common_key)
		message = input("Please enter your message:\n")

		encrypted_message = fernet.encrypt(message.encode()).decode()

		enc_message = {
		"encrypted_message": encrypted_message,
		}
		print(f"Encrypted message: {enc_message}")
		sock.send(json.dumps(enc_message).encode())
		print(f"Encrypted message sent.")
		sock.close()

		save_log()
		

	except socket.error as e:
		print(f"Connection error: {e}")
		return


def unsecure_chat(ip):
	
	print(f"Unsecure chat selected.")
	message_input = input("Please enter your message:\n")

	message = {
	"unencrypted_message": message_input,
	}

	try:
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, socket_number))

		sock.send(json.dumps(message).encode())

		sock.close()
	
		print(f"Unencrypted message sent.")
		save_log()


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

	for ip_address, data in ips.items():
		if data["name"] == in_username:
			ip = ip_address
			break
	else:
		print(f"Username {in_username} not found.")
		return

	if sec_key == "1":
		secure_chat(ip)
	elif sec_key == "2":
		unsecure_chat(ip)
	else:
		print("Invalid chat type code. Enter 1 or 2.")


def main ():

	while True:

		op_code = input("Please enter the operation code:\nUsers (1)\nChat (2)\nHistory (3)\nExit (4)\n")

		if op_code == "1":
			load_users()
		elif op_code == "2":
			load_chat()
		elif op_code == "3":
			print("History")
		elif op_code == "4":
			print("Exiting...")
			break
		else:
			print("Invalid operation code. Enter 1, 2, 3 or 4.")

if __name__ == "__main__":
	main()