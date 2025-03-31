import socket
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import base64

p = 19
g = 2

def uncrypted_message(message):
    print(f"Unencrypted message: {message}")

def fernet_key(key):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=None,
    )
    key_hkdf = hkdf.derive(str(key).encode()) 
    fernet_key = base64.urlsafe_b64encode(key_hkdf)
    return Fernet(fernet_key)

def decrypte_message(encrypted_message, peer_public_key, private_nbr):

    try:
        peer_common_key = (peer_public_key ** int(private_nbr)) % p
        print(f"Peer common key: {peer_common_key}")
        fernet = fernet_key(peer_common_key)
        decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()
        print(f"Decrypted message: {decrypted_message}")
    except Exception as e:
        print(f"Error decrypting message: {e}")

def response_key(private_nbr):
    return (g ** int(private_nbr)) % p

def main():
    print("Welcome to the chat responder!")

    listening_port = 6001
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
                peer_public_key = int(message["key"])
                print(f"Peer public key received: {peer_public_key}")
                private_nbr = input("Please enter the encrypted key number (3 digit): ")
                enc_nbr = response_key(private_nbr)
        

                response_message = json.dumps({"key": enc_nbr})
                conn.send(response_message.encode())
                print(f"Public key sent: {enc_nbr}, waiting for message...")
                data = conn.recv(1024).decode()
                print(f"Message received data: {data}")

                try:
                    message = json.loads(data)

                    if isinstance(message, str):
                        message = json.loads(message)

                except json.JSONDecodeError:
                    print(f"Decoding failed.")
                    return

                if "peer_public_key" in locals() and "private_nbr" in locals():
                    decrypte_message(message["encrypted_message"], peer_public_key, private_nbr)

            elif "unencrypted_message" in message:
                uncrypted_message(message["unencrypted_message"])

            else:
                print(f"Unknown message format:", message)

        except json.JSONDecodeError:
            print(f"Error decoding JSON.")

    conn.close()
    print(f"Connection closed.")

if __name__ == "__main__":
    main()
