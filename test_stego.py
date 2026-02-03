from core.crypto import generate_key, encrypt_data, decrypt_data
from core.stego import embed_data, extract_data

# Sample test data
data = b"Hidden File Transmission Test"

key = generate_key()
encrypted = encrypt_data(key, data)

embed_data("test.png", encrypted, "encoded.png")

extracted = extract_data("encoded.png")
decrypted = decrypt_data(key, extracted)

print("Original:", data)
print("Decrypted:", decrypted)

assert data == decrypted
print("Steganography Test: PASSED")
