from core.crypto import generate_key, encrypt_data, decrypt_data

message = b"Confidential File Content"

key = generate_key()
encrypted = encrypt_data(key, message)
decrypted = decrypt_data(key, encrypted)

print("Original:", message)
print("Encrypted:", encrypted[:50], "...")
print("Decrypted:", decrypted)

assert decrypted == message
print("Encryption Test: PASSED")
