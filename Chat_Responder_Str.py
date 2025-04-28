import socket
import json
import pyDes
import base64
import time
import random

listening_port = 6001

p = 19
g = 2

log_file = "logs.json"

def extend_to_8(data: bytes) -> bytes:
	extra = 8 - (len(data) % 8)
	if extra == 8:
		return data
	return data + b'\x00' * extra

def save_log(op_type, chat_type, message, ip):

    time_now = time.time()

    logs = {
        "time": time_now,
        "ip": ip,
        "op_type": op_type,
        "chat_type": chat_type,
        "message": message,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(logs) + "\n")

    print(f"Log saved.")

def uncrypted_message(message):
    print(f"Unencrypted message: {message}")

def decrypte_message(encrypted_message, peer_public_key, private_nbr):

    try:
        peer_common_key = (peer_public_key ** int(private_nbr)) % p
        print(f"Peer common key: {peer_common_key}")
        decrypted_message = pyDes.triple_des(str(peer_common_key).ljust(24)).decrypt(encrypted_message, padmode=2).decode()
        print(f"Decrypted message: {decrypted_message}")
    except Exception as e:
        print(f"Error decrypting message: {e}")

def response_key(private_nbr):
    return (g ** int(private_nbr)) % p

def main():
    print("Welcome to the chat responder!")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", listening_port))

    while True:

        sock.listen(1)
        print(f"\nListening for incoming messages on port {listening_port}...")
        conn, addr = sock.accept()
        print(f"Connection from {addr} established.")

        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            continue

        try:
            message = json.loads(data)

            if isinstance(message, str):
                message = json.loads(message)

            print(f"\nMessage received")

            if "key" in message:
                save_log("RECEIVED", "Secure", {"key": message["key"]}, addr[0])
                peer_public_key = int(message["key"])
                print(f"Peer public key received: {peer_public_key}")
                private_nbr = random.randint(1, 1000)
                enc_nbr = response_key(private_nbr)
        

                response_message = json.dumps({"key": enc_nbr})
                conn.send(response_message.encode())
                print(f"Public key sent: {enc_nbr}, waiting for message...")

                save_log("SENT", "Secure", {"key": enc_nbr}, addr[0])

                data = conn.recv(1024).decode()
                print(f"Message received data: {data}")

                message = json.loads(data)

                save_log("RECEIVED", "Secure", {"encrypted_message": message["encrypted_message"]}, addr[0])

                if "peer_public_key" in locals() and "private_nbr" in locals():
                    enc_message = eval(message["encrypted_message"])
                    extend_to_8(enc_message)
                    decrypte_message(enc_message, peer_public_key, private_nbr)

            elif "unencrypted_message" in message:
                uncrypted_message(message["unencrypted_message"])
                save_log("RECEIVED", "Unsecure", {"unencrypted_message": message["unencrypted_message"]}, addr[0])

            else:
                print(f"Unknown message format: {message}")

        except json.JSONDecodeError:
            print(f"Error decoding JSON.")
            conn.close()
            print(f"Connection closed.")

if __name__ == "__main__":
    main()
