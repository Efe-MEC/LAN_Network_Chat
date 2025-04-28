import pyDes
import base64

def pad_to_8(data: bytes) -> bytes:
    extra = 8 - (len(data) % 8)
    if extra == 8:
        return data
    return data + b'\x00' * extra

message = "Hello World!"
enc_key = 8

message_bytes = pad_to_8(message.encode())

key = str(enc_key).ljust(24)
cipher = pyDes.triple_des(key)

encrypted_message = cipher.encrypt(message_bytes, padmode=0)
print(f"Encrypted message: {encrypted_message}")

base64_encrypted_message = base64.b64encode(encrypted_message).decode()
print(f"Encrypted message (base64): {base64_encrypted_message}")

string_encrypted_message = str(encrypted_message)
print(f"Encrypted message (string): {string_encrypted_message}")

base64_after_sending = base64.b64decode(base64_encrypted_message.encode())
base64_decrypted_message = cipher.decrypt(base64_after_sending, padmode=0)
print(f"Decrypted message (base64): {base64_decrypted_message.decode()}")


string_after_sending = eval(string_encrypted_message)
string_decrypted_message = cipher.decrypt(string_after_sending, padmode=0)
print(f"Decrypted message (string): {string_decrypted_message.decode()}")
