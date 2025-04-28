import pyDes
import base64

message = "Hello World!"
enc_key = 8

encrypted_message = pyDes.triple_des(str(enc_key).ljust(24)).encrypt(message, padmode=2)

print(f"Encrypted message: {encrypted_message}")
base64_encrypted_message = base64.b64encode(encrypted_message).decode()
print(f"Encrypted message (base64): {base64_encrypted_message}")
string_encrypted_message = str(encrypted_message)
print(f"Encrypted message (string): {string_encrypted_message}")

base64_after_sending = base64.b64decode(base64_encrypted_message.encode())
string_after_sending = string_encrypted_message.encode()

base64_decrypted_message = pyDes.triple_des(str(enc_key).ljust(24)).decrypt(base64_after_sending, padmode=2)
print(f"Decrypted message (base64): {base64_decrypted_message.decode()}")
string_decrypted_message = pyDes.triple_des(str(enc_key).ljust(24)).decrypt(string_after_sending, padmode=2)
print(f"Decrypted message (string): {string_decrypted_message.decode()}")

